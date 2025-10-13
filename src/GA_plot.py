# plot_utils.py
import matplotlib.pyplot as plt

def plot_history(history, max_iter):
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


