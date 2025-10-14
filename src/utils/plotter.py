import matplotlib.pyplot as plt
import os

def confirm_folder(algorithm_name: str):
    folder = f"output/{algorithm_name.lower()}"
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


