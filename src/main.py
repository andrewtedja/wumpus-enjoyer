import json
from utils.plotter import plot_scores, plot_scores_random_restart, plot_sa_results, plot_ga, confirm_folder
from utils.state import init_state, generate_slots
from utils.objective import evaluate
from utils.visualize_timetable import visualize_state

from algorithm.hill_climbing import hill_climbing_steepest, hill_climbing_sideways, hill_climbing_random_restart, hill_climbing_stochastic
from algorithm.simulated_annealing import simulated_annealing
from algorithm.genetic_algorithm import genetic_algorithm

import time, os
import pandas as pd

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("=" * 60)
    print("Tugas Besar 1 IF3170 - Local Search Scheduler")
    print("by Wumpus Enjoyer")
    print("=" * 60)

    # ========================== Read Input (JSON) ==========================
    input_name = input("Masukkan nama file input (tanpa folder, cth: sample_input.json): ").strip()
    input_path = f"input/{input_name}"

    if not os.path.exists(input_path):
        print(f"File '{input_path}' tidak ditemukan. Pastikan file ada di folder 'input/'.")
        exit()

    clear_screen()

    print(f"\nFile input dipilih: {input_path}\n")

    # ========================== Init ==========================

    with open(input_path, "r") as input_file:
        data = json.load(input_file)

    kelas_mata_kuliah = data["kelas_mata_kuliah"]
    ruangan = [ruang["kode"] for ruang in data["ruangan"]]

    slots = generate_slots(ruangan)
    state_awal = init_state(kelas_mata_kuliah, slots)

    # print("[STATE REP] STATE AWAL:")
    # df = pd.DataFrame(list(state_awal.items()), columns=["key", "value"])
    # print(df)

    score = evaluate(state_awal, data)

    print("\n[OBJECTIVE FUNCTION] EVALUATED SCORE: ")
    print("Score total:", score)

    # ========================== SELECT ALGORITHM ==========================
    print("\n[ALGORITHM] Pilihan Algoritma:")
    print("1. Hill Climbing")
    print("2. Hill Climbing with Sideways Move")
    print("3. Hill Climbing with Random Restart")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    print("6. Genetic Algorithm")

    n = int(input("\nMasukkan pilihan algoritma: "))

    # ========================== EXECUTE ==========================
    if n == 1:
        print("\nStarting Hill Climbing...")
        start_time = time.time()
        best_state, best_score, scores = hill_climbing_steepest(state_awal, data, slots, max_iter=1000)
        duration = time.time() - start_time
        algo_name = "Hill Climbing"

    elif n == 2:
        print("\nStarting Hill Climbing with Sideways Move...")
        start_time = time.time()
        best_state, best_score, scores = hill_climbing_sideways(state_awal, data, slots, max_iter=1000, max_side=500)
        duration = time.time() - start_time
        algo_name = "Hill Climbing (Sideways Move)"

    elif n == 3:
        print("\nStarting Hill Climbing with Random Restart...")
        start_time = time.time()
        best_state, best_score, scores = hill_climbing_random_restart(state_awal, data, slots, max_restarts=10, max_iter=1000)
        duration = time.time() - start_time
        algo_name = "Hill Climbing (Random Restart)"

    elif n == 4:
        print("\nStarting Stochastic Hill Climbing...")
        start_time = time.time()
        best_state, best_score, scores = hill_climbing_stochastic(state_awal, data, slots, max_iter=1000, max_attempts=50)
        duration = time.time() - start_time
        algo_name = "Stochastic Hill Climbing"

    elif n == 5:
        print("\nStarting Simulated Annealing...")
        start_time = time.time()
        best_state, best_score, info = simulated_annealing(
            state_awal, data, slots, T0=1000, T_min=1, alpha=0.95,
            target_score=0.0001, patience=500
        )
        duration = time.time() - start_time
        algo_name = "Simulated Annealing"

    elif n == 6:
        pop_size = 30
        max_iter = 300
        print("\nStarting Genetic Algorithm...")
        start_time = time.time()
        best_state, best_score, history = genetic_algorithm(data, slots, pop_size, max_iter)
        duration = time.time() - start_time
        algo_name = "Genetic Algorithm"

    else:
        print("[ERROR] Pilihan tidak valid.")
        exit()

    # ========================== RESULTS ==========================
    # print(f"\n[RESULT] BEST STATE AFTER {algo_name}:")
    # df_best = pd.DataFrame(list(best_state.items()), columns=["key", "value"])
    # print(df_best)

    # HC
    if (n == 1 or n == 2 or n == 4):
        print(f"[INFO] Skor Akhir (Best): {best_score:.3f}")
        print("[INFO] Plot skor telah ditampilkan.")
        plot_scores(scores, f"{algo_name} - Nilai Fungsi Objektif per Iterasi")

    # RR HC
    if n == 3:
        print(f"\n[INFO] Total Restart: {len(scores)}")
        print(f"[INFO] Skor Akhir (Best): {best_score:.3f}")
        print("[INFO] Plot skor telah ditampilkan.")
        plot_scores_random_restart(scores)

    # SA
    if n == 5:
        print(f"\n[INFO] Skor Awal: {info['initial_score']:.3f}")
        print(f"[INFO] Skor Akhir (Best): {best_score:.3f}")
        print("[INFO] Plot E(T) telah ditampilkan.")
        plot_sa_results(info['score_history'], info['boltzmann_history'])

    # GA
    if n == 6:
        print(f"[INFO] Jumlah populasi: {pop_size}")
        print(f"[INFO] Banyak iterasi: {max_iter}")
        print(f"[INFO] Skor Akhir (Best): {best_score:.3f}")
        print("[INFO] Plot E(T) telah ditampilkan.")
        plot_ga(history, max_iter)

    # Visualisasi state awal dan best
    visualize_state(state_awal, ruangan, save_path="input/jadwal-awal.png", show=False)
    visualize_state(state_awal, ruangan, save_path="output/jadwal-best.png", show=False)

    print(f"\n[TIME] Waktu eksekusi: {duration:.3f} detik")
    print(f"[DONE] Visualisasi jadwal (state) awal dan akhir untuk algoritma {algo_name} telah ditampilkan.")