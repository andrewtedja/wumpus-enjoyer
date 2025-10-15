import matplotlib.pyplot as plt
import os

def confirm_folder(algorithm_name: str):
    folder = f"output\{algorithm_name.lower()}"
    os.makedirs(folder, exist_ok=True)
    return folder

# ==================== Hill Climbing ====================

def plot_scores(scores, title, algorithm="hc"):
    folder = confirm_folder(algorithm)
    save_path = os.path.join(folder, f"{algorithm}_plot.png")

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(scores)), scores, marker='o')
    plt.title(title)
    plt.xlabel('Iterasi')
    plt.ylabel('Nilai Fungsi Objektif')
    plt.grid(True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[{algorithm}] Plot saved to {save_path}")


def plot_scores_random_restart(best_scores, algorithm="hc"):
    folder = confirm_folder(algorithm)
    save_path = os.path.join(folder, f"{algorithm}_plot.png")

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(best_scores) + 1), best_scores, marker='o', color='orange')
    plt.title('Best Scores dari Setiap Restart')
    plt.xlabel('Restart ke-')
    plt.ylabel('Best Score')
    plt.grid(True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[{algorithm}] Plot saved to {save_path}")

# ==================== SA ====================

def plot_sa_results(score_history, boltzmann_history, algorithm="sa"):
    folder = confirm_folder(algorithm)
    save_path = os.path.join(folder, f"{algorithm}_plot.png")

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
    print(f"[{algorithm}] Plot saved to {save_path}")

# ==================== Genetic Algorithm ====================

def plot_ga(history, max_iter):
    generations = [h["generation"] for h in history]
    best_scores = [h["best"] for h in history]
    avg_scores = [h["avg"] for h in history]

    if max_iter is not None and len(generations) < max_iter:
        last_best = best_scores[-1] if best_scores else 0
        last_avg = avg_scores[-1] if avg_scores else 0
        for gen in range(len(generations) + 1, max_iter + 1):
            generations.append(gen)
            best_scores.append(last_best)
            avg_scores.append(last_avg)

    plt.figure(figsize=(8, 5))
    plt.plot(generations, best_scores, label="Best Score")
    plt.plot(generations, avg_scores, label="Average Score", linestyle='--')
    plt.xlabel("Generation")
    plt.ylabel("Objective Function")
    plt.title("Genetic Algorithm Graphic Plot")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("genetic-algorithm-result.png")