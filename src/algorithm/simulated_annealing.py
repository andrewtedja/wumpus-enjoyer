import math, random, copy
from utils.objective import evaluate
from .hill_climbing import getNeighbors
import matplotlib.pyplot as plt

'''
NOTES SA:
- Asumsi: ini SA nya mode GA (gradient ascent), bukan GD (gradient descent), jadi neighbor lebi tinggi dari current yang better (higher is better) or maximization
- deltaE = val(current) - val(neighbor)
- Menerima solusi lebih buruk dengan probabilitas -> boltzmann(E(T)) e^(deltaE/T)
- Save riwayat untuk plotting dan frekuensi stuck
'''

# ==================== Boltzmann Function ====================
def boltzmann(deltaE, T) -> float:
    if T <= 0:
        return 0
    try:
        return math.exp(deltaE / T)
    except OverflowError:
        return float('inf')


# ==================== Simulated Annealing ====================
def simulated_annealing(state, data, slots, T_start=1000, T_min=1, alpha=0.95, max_iter=1000):
    current = copy.deepcopy(state)
    current_score = evaluate(current, data)
    best = copy.deepcopy(current)
    best_score = current_score


    # Save history (iter, score, E(T), T)
    T = T_start
    history = []         
    stuck_count = 0
    max_stuck = 0

    for i in range(max_iter):
        if T < T_min:
            break

        neighbor = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        neighbor_score = evaluate(neighbor, data)
        delta = current_score - neighbor_score  

        # Accept
        accept = False
        if delta < 0: 
            accept = True
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                accept = True
        
        if accept:
            current, current_score = neighbor, neighbor_score

        # Track best
        improved = False
        if current_score > best_score: 
            best, best_score = copy.deepcopy(current), current_score
            improved = True

        T *= alpha

        # Stuck Cnter
        if improved:
            stuck_count = 0
        else:
            stuck_count += 1
            max_stuck = max(max_stuck, stuck_count)

        # Logging History
        boltz_score = boltzmann(current_score, T)
        history.append((i, current_score, boltz_score, T))

        print(f"Iter {i+1}: T={T:.2f}, Score={current_score:.2f}, Best={best_score:.2f}")

    print(f"[STUCK SA INFO] Max consecutive stuck iterations: {max_stuck}")

    # Plotting booltzman vs iteration cnt
    plt.plot([h[0] for h in history], [h[2] for h in history])
    plt.title("E(T) terhadap Iterasi (Simulated Annealing - Gradient Ascent)")
    plt.xlabel("Iterasi")
    plt.ylabel("Nilai Boltzmann E(T)")
    plt.grid(True)
    plt.yscale("log")
    plt.show()

    return best, best_score, history
