import json
from utils.plotter import plot_scores, plot_scores_random_restart, plot_sa_results, plot_ga
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

def gabung_jam(jam_list):
    jam_list = sorted(jam_list)
    hasil = []
    start = jam_list[0]
    prev = jam_list[0]
    for j in jam_list[1:]:
        if j == prev + 1:
            prev = j
        else:
            hasil.append((start, prev + 1))
            start = j
            prev = j
    hasil.append((start, prev + 1))
    return hasil

if __name__ == "__main__":
    clear_screen()
    print("╔══════════════════════════════════════════════════════╗")
    print("║ Tugas Besar 1 - Artificial Intelligence              ║")
    print("║ by Wumpus Enjoyer                                    ║")
    print("╚══════════════════════════════════════════════════════╝")

    # ========================== Read Input (JSON) ==========================
    input_name = input("\n> Masukkan nama file input (tanpa folder, cth: sample_input.json): ").strip()
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
    print("╔══════════════════════════════════════════════════════╗")
    print("║ [OBJECTIVE FUNCTION]  EVALUATED SCORE                ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║ Total Score : {score:.2f}                                 ║")
    print("╚══════════════════════════════════════════════════════╝")

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║                 ALGORITHM SELECTION                  ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║ 1. Hill Climbing                                     ║")
    print("║ 2. Hill Climbing with Sideways Move                  ║")
    print("║ 3. Hill Climbing with Random Restart                 ║")
    print("║ 4. Stochastic Hill Climbing                          ║")
    print("║ 5. Simulated Annealing                               ║")
    print("║ 6. Genetic Algorithm                                 ║")
    print("╚══════════════════════════════════════════════════════╝")

    n = int(input("\n> Masukkan pilihan algoritma: "))

    # ========================== EXECUTE ==========================
    if n == 1:
        print("\nStarting Hill Climbing (Steepest)...")
        start_time = time.time()
        final_state, final_score, scores = hill_climbing_steepest(state_awal, data, slots)
        duration = time.time() - start_time
        algo_name = "Hill Climbing (Steepest)"

        print(f"[INFO] Skor Akhir: {final_score:.3f}")
        print(f"[INFO] Jumlah Iterasi: {len(scores)}")
        plot_scores(scores, f"{algo_name} - Nilai Fungsi Objektif per Iterasi")

    elif n == 2:
        max_side = int(input("Masukkan maksimal langkah sideways (default 100): ") or "100")
        print("\nStarting Hill Climbing with Sideways Move...")
        start_time = time.time()
        final_state, final_score, scores = hill_climbing_sideways(state_awal, data, slots, max_side)
        duration = time.time() - start_time
        algo_name = "Hill Climbing (Sideways Move)"

        print(f"[INFO] Skor Akhir: {final_score:.3f}")
        print(f"[INFO] Jumlah Iterasi: {len(scores)}")

        plot_scores(scores, f"{algo_name} - Nilai Fungsi Objektif per Iterasi")

    elif n == 3:
        max_restarts = int(input("Masukkan jumlah maksimal restart (default 10): ") or "10")
        print("\nStarting Hill Climbing with Random Restart...")
        start_time = time.time()
        final_state, final_score, scores, scores_per_restart = hill_climbing_random_restart(data, slots, max_restarts)
        duration = time.time() - start_time
        algo_name = "Hill Climbing (Random Restart)"

        print(f"\n[INFO] Total Restart: {len(scores)}")
        print(f"[INFO] Skor Akhir: {final_score:.3f}")

        plot_scores_random_restart(scores_per_restart, scores)

    elif n == 4:
        max_iter = int(input("Masukkan jumlah maksimal iterasi (default 1000): ") or "1000")
        print("\nStarting Stochastic Hill Climbing...")
        start_time = time.time()
        final_state, final_score, scores = hill_climbing_stochastic(state_awal, data, slots, max_iter)
        duration = time.time() - start_time
        algo_name = "Stochastic Hill Climbing"

        print(f"\n[INFO] Skor Akhir (Final): {final_score:.3f}")
        print(f"[INFO] Jumlah Iterasi: {len(scores)}")
        plot_scores(scores, f"{algo_name} - Nilai Fungsi Objektif per Iterasi")

    elif n == 5:
        user_input = input("Masukkan jumlah maksimal iterasi (kosongkan untuk default (1000)): ").strip()
        if (user_input):
            max_iter = int(user_input)
        else:
            max_iter = 1000
        
        print("\nStarting Simulated Annealing...")
        start_time = time.time()
        info = simulated_annealing(
            state_awal, data, slots, max_iter=max_iter,
            T0=1000, T_min=1, alpha=0.98,
            patience=40
        )

        duration = time.time() - start_time
        algo_name = "Simulated Annealing"

        final_state = info['final_state']
        final_score = info['final_score']

        print(f"\n[INFO] Skor Awal: {info['initial_score']:.3f}")
        print(f"[INFO] Skor Akhir (Final): {final_score:.3f}")
        print(f"[INFO] Jumlah Iterasi: {info['iterations']}")
        print(f"[INFO] Frekuensi Stuck di Local Optima: {info['stuck_events']}")
        print("[INFO] Plot E(T) telah ditampilkan.")

        plot_sa_results(info['score_history'], info['boltzmann_history'])

    elif n == 6:
        pop_size = 30
        max_iter = 300
        print("\nStarting Genetic Algorithm...")
        start_time = time.time()
        final_state, best_score, history = genetic_algorithm(data, slots, pop_size, max_iter)
        duration = time.time() - start_time
        algo_name = "Genetic Algorithm"

        print(f"[INFO] Jumlah populasi: {pop_size}")
        print(f"[INFO] Banyak iterasi: {max_iter}")
        print(f"[INFO] Skor Akhir: {best_score:.3f}")
        print("[INFO] Plot E(T) telah ditampilkan.")
        plot_ga(history, max_iter)

    else:
        print("[ERROR] Pilihan tidak valid.")
        exit()

    # ========================== COMMON POST-PROCESS ==========================

    print(f"\n[TIME] Waktu Eksekusi: {duration:.3f} detik")

    # Visualisasi hasil jadwal
    visualize_state(state_awal, ruangan, save_path="input/jadwal-awal.png", show=False)
    visualize_state(final_state, ruangan, save_path="output/jadwal-final.png", show=False)

    print(f"[DONE] Visualisasi jadwal awal dan akhir untuk algoritma {algo_name} selesai.")

    print("\n[FINAL SCHEDULE]")
    jadwal_per_matkul = {}

    for (hari, jam, ruang), kode in sorted(final_state.items()):
        if kode not in jadwal_per_matkul:
            jadwal_per_matkul[kode] = []
        jadwal_per_matkul[kode].append((hari, jam, ruang))

    urutan_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

    for kode, entries in jadwal_per_matkul.items():
        print(f"\n{kode} - {next((k['nama'] for k in data['kelas_mata_kuliah'] if k['kode'] == kode), 'Tidak diketahui')}")
        by_hari = {}
        for hari, jam, ruang in entries:
            if hari not in by_hari:
                by_hari[hari] = {}
            if ruang not in by_hari[hari]:
                by_hari[hari][ruang] = []
            by_hari[hari][ruang].append(jam)

        for hari in urutan_hari:
            if hari not in by_hari:
                continue
            for ruang, jam_list in by_hari[hari].items():
                for (mulai, selesai) in gabung_jam(jam_list):
                    print(f"  {hari}: {mulai:02d}.00 - {selesai:02d}.00 ({ruang})")
