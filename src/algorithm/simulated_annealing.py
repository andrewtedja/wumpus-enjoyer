import math, random, copy
from utils.objective import evaluate
from .hill_climbing import getSuccessors
import matplotlib.pyplot as plt
import time
import os

'''
NOTES SA:
- deltaE = val(neighbor) - val(current) (Minimization kaya GD)
- Menerima solusi lebih buruk dengan probabilitas -> boltzmann(E(T)) e^(deltaE/T)
- Save riwayat untuk plotting dan frekuensi stuck
'''

# ==================== Boltzmann Function ====================

def schedule(t, T0, alpha):
    return T0 * (alpha ** t)


def boltzmann(deltaE, T) -> float:
    if T <= 0:
        return 0
    try:
        return math.exp(-deltaE / T)
    except OverflowError:
        return float('inf')


def getSuccessor(state, slots, kelas_mata_kuliah):
    filled_slots = list(state.keys())
    if not filled_slots:
        return None

    slot_lama = random.choice(filled_slots)
    kode_kelas = state[slot_lama]

    # nyoba pindahin ke setiap slot lain (baik kosong maupun terisi)
    possible_slots = [slot for slot in slots if slot != slot_lama]
    if not possible_slots:
        return None
    
    slot_baru = random.choice(possible_slots)
    # salin state lama untuk dimodifikasi
    successor = copy.deepcopy(state)

    if slot_baru not in state: # kosong
        # ======================= MOVE =======================
        del successor[slot_lama]
        successor[slot_baru] = kode_kelas
    else: # ada isinya
        # ======================= SWAP =======================
        other_kelas = state[slot_baru]
        successor[slot_lama] = other_kelas
        successor[slot_baru] = kode_kelas

    return successor

# ==================== Simulated Annealing ====================
def simulated_annealing(state, data, slots, T0=1000, T_min=1, alpha=0.95, patience = 50, max_iter=10000):
    current = copy.deepcopy(state)
    current_score = evaluate(current, data)
    # Save history (iter, score, E(T), T)

    best_score = current_score

    score_history = []         
    boltzmann_history = []
    stuck_events = 0
    no_improvement_counter = 0

    t = 0
    T = T0
    while T > T_min and t < max_iter:
        # note: ada tambahan heuristik target_score atau threshold score (0.0001)  
        neighbor = getSuccessor(current, slots, data["kelas_mata_kuliah"])
        neighbor_score = evaluate(neighbor, data)
        
        delta = neighbor_score - current_score
        
        # print(f"Current #{t}:", current_score)
        # print(f"Best: #{t}", best_score)

        print(f"[SA] Iter {t}: Current={current_score}, Best={best_score}, T={T}")

        if delta < 0:  
            boltz_prob = 1.0
        else:  
            boltz_prob = boltzmann(delta, T)

        accept = False
        if delta < 0:
            accept = True
        else:
            rand_val = random.random()
            if rand_val < boltz_prob:
                accept = True

        # Move
        if accept:
            current = neighbor
            current_score = neighbor_score
        
        if current_score < best_score:
            best_score = current_score
            no_improvement_counter = 0
        elif current_score == best_score:
            no_improvement_counter += 1

        if no_improvement_counter >= patience:
            stuck_events += 1
            print(f"[SA] Stuck events #{stuck_events} on iter {t} (no improvement for {patience} iterations)")
            no_improvement_counter = 0


        # Save history
        score_history.append(current_score)
        boltzmann_history.append(boltz_prob)

        # Update
        t += 1
        T = schedule(t, T0, alpha)

        if t % 100 == 0:
            print(f"[Periodic 100 Report] Iter {t} | T={T:.3f} | Score={current_score:.3f}")

        if T <= T_min:
            print(f"[SA] Temperature udah 0 di iterasi {t}")
            break

    return {
        'final_state': current,
        'final_score': current_score,
        'score_history': score_history,
        'boltzmann_history': boltzmann_history,
        'initial_score': score_history[0] if score_history else current_score,
        'stuck_events': stuck_events,
        'iterations': t,
    }