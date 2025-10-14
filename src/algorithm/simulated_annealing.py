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
def simulated_annealing(state, data, slots, T0=1000, T_min=1, alpha=0.95, target_score = 0.0001, patience = 500):

    current = copy.deepcopy(state)
    current_score = evaluate(current, data)
    best_state = copy.deepcopy(current)
    best_score = current_score


    # Save history (iter, score, E(T), T)
    score_history = []         
    boltzmann_history = []
    stuck_count = 0
    max_stuck = 0
    no_improvement_count = 0

    t = 0
    T = T0

    print(f"[SA] Initial Score: {current_score:.4f}")

    while T > T_min and current_score >= target_score:
        neighbor = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        neighbor_score = evaluate(neighbor, data)
        
        delta = neighbor_score - current_score
        
        boltz_prob = boltzmann(delta, T) if delta > 0 else 1.0
        print(boltz_prob)

        accept = False
        if delta < 0:  
            accept = True
        else:  
            if random.random() < boltz_prob:
                accept = True

        if accept:
            current = neighbor
            current_score = neighbor_score

        # Track best solution
        if current_score < best_score:
            best_state = copy.deepcopy(current)
            best_score = current_score
            stuck_count = 0
            no_improvement_count = 0
        else:
            stuck_count += 1
            no_improvement_count += 1
        
        max_stuck = max(max_stuck, stuck_count)

        # Save history
        score_history.append(best_score)
        boltzmann_history.append(boltz_prob)

        if best_score < target_score:
            print(f"[SA] Target score reached at iteration {t}")
            break
        
        if no_improvement_count >= patience:
            print(f"[SA] No improvement for {patience} iterations")
            break

        # Update
        t += 1
        T = schedule(t, T0, alpha)


    # Final report
    print(f"[SA] Final Score: {best_score:.4f}")
    print(f"[SA] Iterations: {t}")
    print(f"[SA] Max Stuck: {max_stuck}")

    # Plotting
    # plot_sa_results(score_history, boltzmann_history)

    return best_state, best_score, {
        'score_history': score_history,
        'boltzmann_history': boltzmann_history,
        'max_stuck': max_stuck,
        'iterations': t,
        'initial_score': score_history[0] if score_history else current_score
    }


# ==================== Plotting ====================

def plot_sa_results(score_history, boltzmann_history, save_path="output/sa_plot.png"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    iterations = list(range(len(score_history)))

    # Plot 1: Objective function (best score) vs iterasi
    ax1.plot(iterations, score_history, 'b-', linewidth=2)
    ax1.set_xlabel('Iterasi')
    ax1.set_ylabel('Objective Function (Best Score)')
    ax1.set_title('Nilai Objective Function terhadap Iterasi')
    ax1.grid(True, alpha=0.3)

    # Plot 2: boltzmann vs iterasi
    ax2.plot(iterations, boltzmann_history, 'r-', linewidth=1)
    ax2.set_xlabel('Iterasi')
    ax2.set_ylabel('e^(-deltaE/T)')
    ax2.set_title('Probabilitas Boltzmann terhadap Iterasi')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(save_path, dpi=300)
    plt.close(fig) 
    print(f"[SA] Plot saved to {save_path}")