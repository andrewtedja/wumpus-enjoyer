import copy
import random
from utils.objective import evaluate

def getNeighbors(state, slots, kelas_mata_kuliah):
    import copy, random
    neighbor_state = copy.deepcopy(state)
    unique_classes = list(set(state.values()))
    rand_num = random.random()

    if rand_num < 0.5:
        # ===== MOVE =====
        kode_kelas = random.choice(unique_classes)
        # pilih 1 slot lama dari kelas tsb
        slot_lama = random.choice([s for s, v in state.items() if v == kode_kelas])

        # hapus slot lama
        del neighbor_state[slot_lama]

        # pilih slot baru (boleh bentrok biar Objective 2 bisa aktif)
        slot_baru = random.choice(slots)
        neighbor_state[slot_baru] = kode_kelas

        return neighbor_state

    else:
        # ===== SWAP =====
        if len(unique_classes) < 2:
            return neighbor_state

        kelas1, kelas2 = random.sample(unique_classes, 2)
        slot_kelas1 = [s for s, v in state.items() if v == kelas1]
        slot_kelas2 = [s for s, v in state.items() if v == kelas2]

        if not slot_kelas1 or not slot_kelas2:
            return neighbor_state

        # pilih 1 slot dari masing-masing kelas
        slot1 = random.choice(slot_kelas1)
        slot2 = random.choice(slot_kelas2)

        # tukar isinya langsung
        neighbor_state[slot1], neighbor_state[slot2] = neighbor_state[slot2], neighbor_state[slot1]

        return neighbor_state

def hill_climbing_steepest(state, data, slots, max_iter=1000):
    current = state
    current_score = evaluate(current, data)
    visited = {tuple(sorted(current.items()))}
    scores = [current_score]

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")

    for step in range(max_iter):
        attempts = 0
        candidate = None

        # cari 1 neighbor yang valid
        while attempts < 100:
            attempts += 1
            print(f"[DEBUG] Percobaan neighbor ke-{attempts}")
            neighbor = getNeighbors(current, slots, data["kelas_mata_kuliah"])
            if neighbor is None:
                print("[DEBUG] Tetangga yang dihasilkan tidak ada, coba lagi.")
                continue

            signature = tuple(sorted(neighbor.items()))
            if signature in visited:
                print("[DEBUG] Tetangga sudah pernah dikunjungi, coba lagi.")
                continue

            candidate = neighbor
            visited.add(signature)
            print("[DEBUG] Tetangga valid ditemukan.")
            break

        # tidak ada tetangga baru
        if candidate is None:
            print("[STOP] Tidak ada tetangga valid ditemukan, berhenti.")
            break

        neighbor_score = evaluate(candidate, data)
        print(f"[STEP {step+1}] Current={current_score}, Neighbor={neighbor_score}")

        # evaluasi hasil
        if neighbor_score < current_score:
            current, current_score = candidate, neighbor_score
            scores.append(current_score)
        elif neighbor_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            current, current_score = candidate, neighbor_score
            scores.append(current_score)
            break
        else:
            print("[STOP] Tidak ada perbaikan lebih lanjut, berhenti.")
            break

    return current, current_score, scores



def hill_climbing_sideways(state, data, slots, max_iter=1000, max_side=20):
    current = state
    current_score = evaluate(current, data)
    visited = {tuple(sorted(current.items()))}
    scores = [current_score]
    side_count = 0

    print(f"[INIT] Nilai fungsi objektif awal = {current_score}")

    for step in range(max_iter):
        attempts = 0
        candidate = None

        # cari 1 neighbor yang valid
        while attempts < 100:
            attempts += 1
            print(f"[DEBUG] Percobaan neighbor ke-{attempts}")
            neighbor = getNeighbors(current, slots, data["kelas_mata_kuliah"])
            if neighbor is None:
                print("[DEBUG] Tetangga yang dihasilkan tidak ada, coba lagi.")
                continue

            signature = tuple(sorted(neighbor.items()))
            if signature in visited:
                print("[DEBUG] Tetangga sudah pernah dikunjungi, coba lagi.")
                continue

            candidate = neighbor
            visited.add(signature)
            print("[DEBUG] Tetangga valid ditemukan.")
            break

        if candidate is None:
            print("[STOP] Tidak ada tetangga valid ditemukan, berhenti.")
            break

        neighbor_score = evaluate(candidate, data)
        print(f"[STEP {step+1}] Current={current_score}, Neighbor={neighbor_score}, Sideways={side_count}")

        # evaluasi hasil
        if neighbor_score < current_score:
            current, current_score = candidate, neighbor_score
            scores.append(current_score)
            side_count = 0
        elif neighbor_score == current_score and side_count < max_side:
            print(f"[SIDEWAYS] Langkah datar ke-{side_count+1}")
            current, current_score = candidate, neighbor_score
            scores.append(current_score)
            side_count += 1
        elif neighbor_score <= 0:
            print("[DONE] Solusi optimal ditemukan.")
            current, current_score = candidate, neighbor_score
            scores.append(current_score)
            break
        else:
            print("[STOP] Tidak ada perbaikan lebih lanjut, berhenti.")
            break

    return current, current_score, scores

def hill_climbing_random_restart(state, data, slots, max_restarts=10, max_iter=1000):
    best_state = state
    best_score = evaluate(state, data)
    best_scores = []

    for restart in range(max_restarts):
        print(f"Restart {restart+1}")
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


        new_state, new_score, scores = hill_climbing_steepest(initial_state, data, slots, max_iter=max_iter)
        best_scores.append(new_score)
        if new_score < best_score:
            best_state, best_score = new_state, new_score

    return best_state, best_score, best_scores

def hill_climbing_stochastic(state, data, slots, max_iter=1000, max_attempts=50):
    current = state
    current_score = evaluate(current, data)
    visited = {tuple(sorted(current.items()))}  # simpan bentuk hash
    scores = [current_score]

    print(f"[INIT] Score awal = {current_score}")

    for step in range(max_iter):
        neighbor = None
        attempts = 0

        # generate neighbor yang belum pernah diambil
        while attempts < max_attempts:
            print(f"[DEBUG] Mencari tetangga valid, percobaan ke-{attempts+1}")
            attempts += 1
            candidate = getNeighbors(current, slots, data["kelas_mata_kuliah"])
            if candidate is None:
                print("[DEBUG] Tetangga yang dihasilkan tidak ada, coba lagi.")
                continue

            key = tuple(sorted(candidate.items()))
            if key not in visited:
                neighbor = candidate
                visited.add(key)
                break
            else:
                print("[DEBUG] Tetangga sudah pernah dikunjungi, coba lagi.")
                continue

        # kalau gak ada neighbor baru
        if neighbor is None:
            print(f"[STOP] Tidak ada neighbor baru setelah {max_attempts} percobaan.")
            break

        neighbor_score = evaluate(neighbor, data)
        scores.append(neighbor_score)
        print(f"[STEP {step}] Score {current_score} → {neighbor_score}")

        # kalo neighbor lebih bagus, pindah ke neighbor
        if neighbor_score < current_score:
            current, current_score = neighbor, neighbor_score
        else:
            pass

        # stop duluan kalo udah optimal
        if current_score <= 0:
            print(f"[DONE] Solusi optimal ditemukan di iter {step}")
            break

    return current, current_score, scores
