import json
from utils.state import init_state, generate_slots, get_empty_slots
from utils.objective import evaluate
from algorithm.hill_climbing import hill_climbing_steepest, hill_climbing_sideways, hill_climbing_random_restart, hill_climbing_stochastic
from algorithm.simulated_annealing import simulated_annealing

import pandas as pd

if __name__ == "__main__":
    
    # ========================== Read Input (JSON) ==========================
    with open("data/sample_input.json", "r") as input_file:
        data = json.load(input_file)

    kelas_mata_kuliah = data["kelas_mata_kuliah"]
    ruangan = [ruang["kode"] for ruang in data["ruangan"]]

    slots = generate_slots(ruangan)
    state = init_state(kelas_mata_kuliah, slots)

    # ========================== PRINT TIME TABLE ==========================
    print("[STATE REP] STATE AWAL:")
    df = pd.DataFrame(list(state.items()), columns=["key", "value"])
    print(df)

    score = evaluate(state, data)

    print("\n[OBJ FUNCTION] EVALUATED SCORE: ")
    print("Score total:", score)

    # ========================== SELECT ALGORITHM ==========================
    print("\n[ALGORITHM] Pilihan Algoritma:")
    print("1. Hill Climbing")
    print("2. Hill Climbing with Sideways Move")
    print("3. Hill Climbing with Random Restart")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")

    n = int(input("\nMasukkan pilihan algoritma: "))

    # ========================== EXECUTE ==========================
    if n == 1:
        print("\nStarting Hill Climbing...")
        best_state, best_score = hill_climbing_steepest(state, data, slots, max_iter=1000)
        algo_name = "Hill Climbing"
    elif n == 2:
        print("\nStarting Hill Climbing with Sideways Move...")
        best_state, best_score = hill_climbing_sideways(state, data, slots, max_iter=1000, max_side=500)
        algo_name = "Hill Climbing (Sideways Move)"
    elif n == 3:
        print("\nStarting Hill Climbing with Random Restart...")
        best_state, best_score = hill_climbing_random_restart(state, data, slots, max_restarts=10, max_iter=1000)
        algo_name = "Hill Climbing (Random Restart)"
    elif n == 4:
        print("\nStarting Stochastic Hill Climbing...")
        best_state, best_score = hill_climbing_stochastic(state, data, slots, max_iter=1000, max_attempts=50)
        algo_name = "Stochastic Hill Climbing"
    elif n == 5:
        print("\nStarting Simulated Annealing (Gradient Ascent Mode)...")
        best_state, best_score, history = simulated_annealing(state, data, slots, T_start=1000, T_min=1, alpha=0.95, max_iter=1000)
        algo_name = "Simulated Annealing"
    else:
        print("[ERROR] Pilihan tidak valid.")
        exit()

    # ========================== RESULTS ==========================
    print(f"\n[RESULT] BEST STATE AFTER {algo_name}:")
    df_best = pd.DataFrame(list(best_state.items()), columns=["key", "value"])
    print(df_best)
    print("Best Score:", best_score)

    if n == 3:
        print(f"\n[INFO] Total Iterasi SA: {len(history)}")
        print(f"[INFO] Skor Akhir (Best): {best_score:.3f}")
        print("[INFO] Plot E(T) telah ditampilkan.")
