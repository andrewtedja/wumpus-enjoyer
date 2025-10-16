import copy
import random
from utils.objective import evaluate

def getNeighbors(state, slots, kelas_mata_kuliah):
    neighbors = []
    filled_slots = list(state.keys())
    empty_slots = [slot for slot in slots if slot not in state]

    # ======================= MOVE =======================
    for slot_lama in filled_slots:
        kode_kelas = state[slot_lama]
        for slot_baru in empty_slots:
            neighbor = copy.deepcopy(state)
            # pindahkan kelas dari slot_lama ke slot_baru
            del neighbor[slot_lama]
            neighbor[slot_baru] = kode_kelas
            neighbors.append(neighbor)

    # ======================= SWAP =======================
    for i in range(len(filled_slots)):
        for j in range(i + 1, len(filled_slots)):
            slot1, slot2 = filled_slots[i], filled_slots[j]
            if state[slot1] == state[slot2]:
                continue  # gak perlu swap kelas yang sama

            neighbor = copy.deepcopy(state)
            # tukar kelas di slot1 dan slot2
            neighbor[slot1], neighbor[slot2] = neighbor[slot2], neighbor[slot1]
            neighbors.append(neighbor)

    return neighbors

def hill_climbing_steepest(state, data, slots):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")
    step = 0

    while current_score > 0:
        step += 1
        neighbors = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        if not neighbors:
            print("[STOP] Tidak ada tetangga ditemukan.")
            break

        # evaluasi semua tetangga
        scored_neighbors = [(evaluate(n, data), n) for n in neighbors]
        scored_neighbors.sort(key=lambda x: x[0])  # ambil skor terkecil
        best_score, best_neighbor = scored_neighbors[0]

        print(f"[STEP {step+1}] Current={current_score}, BestNeighbor={best_score}")

        # kalau gak ada perbaikan, stop
        if best_score >= current_score:
            print("[STOP] Tidak ada perbaikan lebih lanjut (local optimum).")
            break

        # update
        current, current_score = best_neighbor, best_score
        scores.append(current_score)

        if current_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            break

    return current, current_score, scores


def hill_climbing_sideways(state, data, slots, max_side=20):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]
    side_count = 0

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")

    step = 0
    while current_score > 0:
        step += 1
        neighbors = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        if not neighbors:
            print("[STOP] Tidak ada tetangga ditemukan.")
            break

        scored_neighbors = [(evaluate(n, data), n) for n in neighbors]
        scored_neighbors.sort(key=lambda x: x[0])
        best_score, best_neighbor = scored_neighbors[0]

        print(f"[STEP {step+1}] Current={current_score}, BestNeighbor={best_score}, Sideways={side_count}")

        # jika skor lebih baik
        if best_score < current_score:
            current, current_score = best_neighbor, best_score
            scores.append(current_score)
            side_count = 0
        # jika skor sama, boleh jalan datar
        elif best_score == current_score and side_count < max_side:
            side_count += 1
            current, current_score = best_neighbor, best_score
            scores.append(current_score)
            print(f"[SIDEWAYS] Langkah datar ke-{side_count}")
        else:
            print("[STOP] Tidak ada perbaikan lebih lanjut, berhenti.")
            break

        if current_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            break

    return current, current_score, scores

def hill_climbing_random_restart(data, slots, max_restarts=10):
    best_state = None
    best_score = float('inf')
    best_scores = []

    for restart in range(max_restarts):
        print(f"\n[RESTART {restart+1}]")
        # generate state acak
        initial_state = {}
        kelas_list = data["kelas_mata_kuliah"]
        random.shuffle(kelas_list)

        for kelas in kelas_list:
            kode = kelas["kode"]
            sks = kelas["sks"]
            placed = False
            random_slots = slots[:]
            random.shuffle(random_slots)

            for (hari, jam, ruang) in random_slots:
                if (hari, jam, ruang) not in initial_state:
                    initial_state[(hari, jam, ruang)] = kode
                    if list(initial_state.values()).count(kode) == sks:
                        placed = True
                        break

        # jalankan steepest ascent
        final_state, final_score, _ = hill_climbing_steepest(initial_state, data, slots)
        best_scores.append(final_score)

        if final_score < best_score:
            best_score = final_score
            best_state = final_state

        print(f"[RESTART {restart+1}] Score akhir = {final_score}")
        if final_score == 0:
            print("[DONE] Solusi optimal ditemukan, berhenti restart.")
            break

    print(f"\n[FINAL] Skor terbaik dari semua restart = {best_score}")
    return best_state, best_score, best_scores

def hill_climbing_stochastic(state, data, slots, max_iter=1000):
    current = state
    current_score = evaluate(current, data)
    scores = [current_score]

    print(f"[INIT] Score awal = {current_score}")

    for step in range(max_iter):
        neighbors = getNeighbors(current, slots, data["kelas_mata_kuliah"])
        if not neighbors:
            print("[STOP] Tidak ada tetangga ditemukan.")
            break

        # ambil tetangga yang lebih baik dari current
        better_neighbors = [n for n in neighbors if evaluate(n, data) < current_score]

        if not better_neighbors:
            print("[STOP] Tidak ada neighbor yang lebih baik, berhenti.")
            break

        # pilih 1 random dari yang lebih baik
        next_state = random.choice(better_neighbors)
        next_score = evaluate(next_state, data)
        print(f"[STEP {step+1}] {current_score} -> {next_score}")


        if next_score < current_score:
            current, current_score = next_state, next_score
            scores.append(current_score)
            print(f"[UPDATE] Score diperbarui menjadi {current_score}")
        else:
            print("[NO UPDATE] Score tidak berubah.")

        if current_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            break

    return current, current_score, scores