import math, random, copy
from utils.objective import evaluate
from .hill_climbing import getNeighbors
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


# ==================== Simulated Annealing ====================
def simulated_annealing(state, data, slots, T0=1000, T_min=1, alpha=0.95, patience = 500, max_iter=10000):

    current = copy.deepcopy(state)
    current_score = evaluate(current, data)


    # Save history (iter, score, E(T), T)
    score_history = []         
    boltzmann_history = []
    stuck_count = 0
    stuck_events = 0
    no_improvement_count = 0

    t = 0
    T = T0

    print(f"[SA] Initial Score: {current_score:.4f}")

    while T > T_min and t < max_iter:
        # note: ada tambahan heuristik target_score atau threshold score (0.0001)  
        neighbor = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        neighbor_score = evaluate(neighbor, data)
        
        delta = neighbor_score - current_score
        
        boltz_prob = boltzmann(delta, T) if delta > 0 else 1.0
        # print(boltz_prob)

        accept = False
        if delta < 0:  
            accept = True
        else:  
            if random.random() < boltz_prob:
                accept = True

        if accept:
            current = neighbor
            current_score = neighbor_score
            
            no_improvement_count = 0

            if stuck_count > 0:
                stuck_events += 1
            stuck_count = 0
        else:
            stuck_count += 1
            no_improvement_count += 1
        

        # Save history
        score_history.append(current_score)
        boltzmann_history.append(boltz_prob)

        if no_improvement_count >= patience:
            print(f"[SA] No improvement for {patience} iterations")
            break

        # Update
        t += 1
        T = schedule(t, T0, alpha)

        if t % 100 == 0:
            print(f"[Periodic 100 Report] Iter {t} | T={T:.3f} | Score={current_score:.3f}")


        if T <= T_min:
            print(f"[SA] Temperature udah 0 di iterasi {t}")
            break


    # Final report
    # print(f"[SA] Final Score: {current_score:.3f}")
    # print(f"[SA] Iterations: {t}, Max Iterations: {max_iter}")

    return {
        'final_state': current,
        'final_score': current_score,
        'score_history': score_history,
        'boltzmann_history': boltzmann_history,
        'initial_score': score_history[0] if score_history else current_score,
        'stuck_events': stuck_events,
        'iterations': t,
    }