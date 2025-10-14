import pandas as pd
import random
import copy
import time
from typing import List, Dict, Tuple, Any
from utils.state import init_state, get_empty_slots, generate_slots, hari_list, jam_list
from utils.objective import evaluate
from utils.GA_utils import *

def fitness_function(score: float) -> float:
    return 1.0 / (1.0 + score)

def roulette_wheel_selection(population: List[Dict], scores: List[float]) -> Dict:
    fitnesses = [fitness_function(s) for s in scores]
    total_fitness = sum(fitnesses)

    if total_fitness == 0:
        return copy.deepcopy(random.choice(population))

    probabilities = [f / total_fitness for f in fitnesses]

    # Roulette wheel, LETS GO GAMBLING
    rand = random.random()
    cumulative = 0.0
    for ind, prob in zip(population, probabilities):
        cumulative += prob
        if rand <= cumulative:
            return copy.deepcopy(ind)

    return copy.deepcopy(population[-1])


def crossover(parent1: Dict[Tuple[str,int,str], str],
              parent2: Dict[Tuple[str,int,str], str],
              kelas_mata_kuliah: List[Dict],
              slots_all: List[Tuple[str,int,str]],
              crossover_rate: float = 0.8) -> Tuple[Dict, Dict]:
    
    if random.random() > crossover_rate:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    child1 = {}
    child2 = {}

    # mapping kode dengan sks
    dict_sks = {k["kode"]: k["sks"] for k in kelas_mata_kuliah}
    kelas_codes = [k["kode"] for k in kelas_mata_kuliah]

    # pilih subset
    cut_frac = random.uniform(0.2, 0.6)  # random fraction to take
    take_count = max(1, int(cut_frac * len(kelas_codes)))
    take_from_p1 = set(random.sample(kelas_codes, take_count))

    # salin kode matkul dari source ke target kalau slotnya kosong
    def attempt_copy(source, target, take_set):
        used = set()
        for kode in take_set:
            src_slots = get_slots(source, kode)
            if not src_slots:
                continue
            # skip slot bentrok atau berisi
            conflict = any(slot in used for slot in src_slots)
            if conflict:
                continue
            # tambah slot kode matkul ke anak 
            for slot in src_slots:
                target[slot] = kode
                used.add(slot)
        return used

    # tuker subset
    used1 = attempt_copy(parent1, child1, take_from_p1)
    used2 = attempt_copy(parent2, child2, take_from_p1)  

    remaining_for_child1 = [kode for kode in kelas_codes if kode not in take_from_p1]
    remaining_for_child2 = [kode for kode in kelas_codes if kode in take_from_p1]

    # isi kelas yang blom ada dari parent lain / random posisi
    def fill_child(child, remaining, other_parent):
        for kode in remaining:
            sks = dict_sks[kode]
            src_slots = get_slots(other_parent, kode)
            if src_slots:
                if all(slot not in child for slot in src_slots):
                    for slot in src_slots:
                        child[slot] = kode
                    continue
            # klo bentrok, dapet slot random yg ksoong
            valid_starts = find_initial_position(slots_all, child, sks)
            if not valid_starts:
                continue
            start = random.choice(valid_starts)
            add_code(child, kode, start, sks)

    fill_child(child1, remaining_for_child1, parent2)
    fill_child(child2, remaining_for_child2, parent1)

    def ensure_complete(child):
        missing = [kode for kode in kelas_codes if not get_slots(child, kode)]
        for kode in missing:
            sks = dict_sks[kode]
            valid_starts = find_initial_position(slots_all, child, sks)
            if valid_starts:
                start = random.choice(valid_starts)
                add_code(child, kode, start, sks)
            else:
                return None
        return child

    child1 = ensure_complete(child1)
    child2 = ensure_complete(child2)

    # klo gabisa, balik ke parent
    if child1 is None:
        try:
            child1 = init_state(kelas_mata_kuliah, slots_all)
        except Exception:
            child1 = copy.deepcopy(parent1)
    if child2 is None:
        try:
            child2 = init_state(kelas_mata_kuliah, slots_all)
        except Exception:
            child2 = copy.deepcopy(parent2)

    if not is_valid_duration(child1, {"kelas_mata_kuliah": kelas_mata_kuliah}):
        child1 = init_state(kelas_mata_kuliah, slots_all)
    if not is_valid_duration(child2, {"kelas_mata_kuliah": kelas_mata_kuliah}):
        child2 = init_state(kelas_mata_kuliah, slots_all)


    return child1, child2

def mutate(state: Dict[Tuple[str,int,str], str],
           kelas_mata_kuliah: List[Dict],
           slots_all: List[Tuple[str,int,str]],
           mutation_rate: float = 0.05) -> Dict:
 
    child = copy.deepcopy(state)
    # mapping kode dengan sks
    dict_sks = {k["kode"]: k["sks"] for k in kelas_mata_kuliah}
    if random.random() > mutation_rate:
        return child

    # pilih 1 atau 2 kelas untuk di mutasi
    n_mut = random.choice([1, 1, 2]) # lebih ke 1  
    kelas_codes = [k["kode"] for k in kelas_mata_kuliah]
    for _ in range(n_mut):
        kode = random.choice(kelas_codes)
        sks = dict_sks[kode]
        remove_code(child, kode)
        valid_starts = find_initial_position(slots_all, child, sks)
        if not valid_starts:
            continue
        start = random.choice(valid_starts)
        add_code(child, kode, start, sks)

    if not is_valid_duration(child, {"kelas_mata_kuliah": kelas_mata_kuliah}):
        child = init_state(kelas_mata_kuliah, slots_all)

    return child

def genetic_algorithm(data: Dict[str, Any],
                      slots: List[Tuple[str,int,str]],
                      pop_size: int = 3,
                      max_iter: int = 100,
                      crossover_rate: float = 0.8,
                      mutation_rate: float = 0.05,
                      elitism: int = 1,
                      verbose: bool = False) -> Tuple[Dict, float, List[Dict]]:
    kelas_mata_kuliah = data["kelas_mata_kuliah"]

    population = []
    attempts = 0
    while len(population) < pop_size and attempts < pop_size * 5:
        try:
            ind = init_state(kelas_mata_kuliah, slots)
            population.append(ind)
        except Exception:
            attempts += 1
            continue
    if len(population) < pop_size:
        while len(population) < pop_size:
            population.append(copy.deepcopy(population[-1]))

    scores = [evaluate(ind, data) for ind in population]
    best_idx = min(range(len(scores)), key=lambda i: scores[i])
    best_state = copy.deepcopy(population[best_idx])
    best_score = scores[best_idx]

    history = []
    start_time = time.time()

    if verbose:
        print(f"[GA] Init pop_size={pop_size}, max_iter={max_iter}, best_score_init={best_score:.4f}")

    for gen in range(1, max_iter + 1):
        new_population = []

        ranked = sorted(list(zip(population, scores)), key=lambda x: x[1])
        elites = [copy.deepcopy(p) for p, s in ranked[:elitism]]
        for e in elites:
            new_population.append(e)

        while len(new_population) < pop_size:
            parent1 = roulette_wheel_selection(population, scores)
            parent2 = roulette_wheel_selection(population, scores)

            child1, child2 = crossover(parent1, parent2, kelas_mata_kuliah, slots, crossover_rate=crossover_rate)

            child1 = mutate(child1, kelas_mata_kuliah, slots, mutation_rate=mutation_rate)
            child2 = mutate(child2, kelas_mata_kuliah, slots, mutation_rate=mutation_rate)
            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        # tuker populasi
        population = new_population
        scores = [evaluate(ind, data) for ind in population]
        gen_best_idx = min(range(len(scores)), key=lambda i: scores[i])
        gen_best_score = scores[gen_best_idx]
        gen_avg_score = sum(scores) / len(scores)

        # ngeupdate global stats
        if gen_best_score < best_score:
            best_score = gen_best_score
            best_state = copy.deepcopy(population[gen_best_idx])
            best_fitness = fitness_function(best_score)

        history.append({"generation": gen, "best": gen_best_score, "avg": gen_avg_score})

        if verbose:
            print(f"[GA] Gen {gen:03d} | best_score={gen_best_score:.4f} | best_fitness={fitness_function(gen_best_score):.4f}")

        if best_score <= 0:
            if verbose:
                print(f"[GA] Found perfect solution at generation {gen}")
            break

    elapsed = time.time() - start_time
    if verbose:
        print(f"[GA] Done. Best score={best_score:.4f}, time={elapsed:.2f}s")

    return best_state, best_score, history
