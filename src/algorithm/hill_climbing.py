import copy
import random
from utils.objective import evaluate

def getSuccessors(state, slots, kelas_mata_kuliah):
    succesors = []
    filled_slots = list(state.keys())

    for slot_lama in filled_slots:
        kode_kelas = state[slot_lama]

        # nyoba pindahin ke setiap slot lain (baik kosong maupun terisi)
        for slot_baru in slots:
            if slot_baru == slot_lama:
                continue  

            succesor = copy.deepcopy(state)

            if slot_baru not in state: # Kosong
                # ======================= MOVE =======================
                # hapus dari slot lama, pindahkan ke slot baru (kosong)
                del succesor[slot_lama]
                succesor[slot_baru] = kode_kelas
            else: # Filled
                # ======================= SWAP =======================
                # slot_baru terisi -> tukar isi dua slot
                other_kelas = state[slot_baru]
                succesor[slot_lama] = other_kelas
                succesor[slot_baru] = kode_kelas

            succesors.append(succesor)

    return succesors

# Steepest HC (terminate on peak/flat)
def hill_climbing_steepest(state, data, slots):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")
    step = 0
    
    while current_score > 0:
        step += 1
        succesors = getSuccessors(current, slots, data["kelas_mata_kuliah"])
        if not succesors:
            print("[STOP] Tidak ada tetangga ditemukan.")
            break

        evaluated = [(evaluate(n, data), n) for n in succesors]
        evaluated.sort(key=lambda x: x[0])  # ambil skor terkecil
        best_score, best_state = evaluated[0]

        print(f"[STEP {step+1}] Current={current_score}, CurrentBestSucc={best_score}")

        # stop condition (successor same or worse)
        all_worse_or_equal = all(score >= current_score for score, _ in evaluated)
        if all_worse_or_equal:
            print("[STOP] Semua successor sama atau lebih buruk (local optimum tercapai).")
            break

        # update
        current, current_score = best_state, best_score
        scores.append(current_score)

        if current_score <= 0:
            print("[DONE] Solusi global optimal ditemukan.")
            break

    return current, current_score, scores

# Sideways HC (terminate on peak)
def hill_climbing_sideways(state, data, slots, max_side=100):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]
    side_count = 0

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")

    step = 0
    while current_score > 0:
        step += 1
        successors = getSuccessors(current, slots, data["kelas_mata_kuliah"])
        if not successors:
            print("[STOP] Tidak ada successor ditemukan.")
            break

        evaluated = [(evaluate(s, data), s) for s in successors]
        evaluated.sort(key=lambda x: x[0])
        best_score, best_state = evaluated[0]

        print(f"[STEP {step}] Current={current_score}, BestNeighbor={best_score}, Sideways={side_count}")

        # stop condition (successor worse, same masih diambil until max_side)
        all_worse = all(score > current_score for score, _ in evaluated)
        all_equal = all(score == current_score for score, _ in evaluated)

        if all_worse or (all_equal and side_count >= max_side):
            print("[STOP] Semua successor lebih buruk atau sudah melewati batas max_side.")
            break

        if best_score < current_score:
            current, current_score = best_state, best_score
            scores.append(current_score)
            side_count = 0
        elif best_score == current_score and side_count < max_side:
            side_count += 1
            current, current_score = best_state, best_score
            scores.append(current_score)
            print(f"[SIDEWAYS] Langkah datar ke-{side_count}")
        else:
            print("[STOP] Tidak ada perbaikan lebih lanjut, berhenti.")
            break


        if current_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            break

    return current, current_score, scores

# RANDOM RESTART HC
def hill_climbing_random_restart(data, slots, max_restarts=10):
    best_state = None
    best_score = float('inf')
    best_scores = []

    for restart in range(max_restarts):
        print(f"\n[RESTART {restart+1}]")
        # generate state acak
        initial_state = {}
        kelas_list = data["kelas_mata_kuliah"]
        random.shuffle(kelas_list)

        for kelas in kelas_list:
            kode = kelas["kode"]
            sks = kelas["sks"]
            placed = False
            random_slots = slots[:]
            random.shuffle(random_slots)

            for (hari, jam, ruang) in random_slots:
                if (hari, jam, ruang) not in initial_state:
                    initial_state[(hari, jam, ruang)] = kode
                    if list(initial_state.values()).count(kode) == sks:
                        placed = True
                        break

        # jalankan steepest ascent
        final_state, final_score, _ = hill_climbing_steepest(initial_state, data, slots)
        best_scores.append(final_score)

        if final_score < best_score:
            best_score = final_score
            best_state = final_state

        print(f"[RESTART {restart+1}] Score terbaik = {final_score}")

    print(f"\n[FINAL] Skor terbaik dari semua restart = {best_score}")
    return best_state, best_score, best_scores

# Stochastic HC (terminate on flat)
def hill_climbing_stochastic(state, data, slots, max_iter=1000):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]

    print(f"[INIT] Score awal = {current_score}")

    for step in range(max_iter):
        successor = getSuccessors(current, slots, data["kelas_mata_kuliah"])
        if not successor:
            print("[STOP] Tidak ada tetangga ditemukan.")
            break

        # ambil tetangga yang lebih baik dari current
        better_successor = [n for n in successor if evaluate(n, data) < current_score]

        if not better_successor:
            print("[STOP] Tidak ada neighbor yang lebih baik, berhenti.")
            break

        # pilih 1 random dari yang lebih baik
        next_state = random.choice(better_successor)
        next_score = evaluate(next_state, data)
        print(f"[STEP {step+1}] {current_score} -> {next_score}")

        current, current_score = next_state, next_score
        scores.append(current_score)

        if current_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            break

    return current, current_score, scores