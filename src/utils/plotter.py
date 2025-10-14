import matplotlib.pyplot as plt

def plot_scores(scores, title):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(scores)), scores, marker='o')
    plt.title(title)
    plt.xlabel('Iterasi')
    plt.ylabel('Nilai Fungsi Objektif')
    plt.grid(True)
    plt.savefig("src/data/HC_plot.png")
    plt.show()

def plot_scores_random_restart(best_scores):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(best_scores) + 1), best_scores, marker='o', color='orange')
    plt.title('Best Scores dari Setiap Restart')
    plt.xlabel('Restart ke-')
    plt.ylabel('Best Score')
    plt.grid(True)
    plt.savefig("src/data/HC_RR_plot.png")
    plt.show()