import copy
import random
from objective import evaluate

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


def hill_climbing_sideways(state, data, slots, max_iter=1000, max_side=20):
    current = state
    current_score = evaluate(current, data)
    side_count = 0
    visited = {tuple(sorted(current.items()))}
    
    for step in range(max_iter):
        neighbors = []
        attempts = 0
        seen_candidates = set()
        while not neighbors and attempts < 100:
            candidate = getNeighbors(current, slots, data["kelas_mata_kuliah"])
            attempts += 1
            if candidate is None:
                continue
            signature = tuple(sorted(candidate.items()))
            if signature in visited or signature in seen_candidates:
                continue
            neighbors.append(candidate)
            seen_candidates.add(signature)
        if not neighbors:
            print("[DEBUG] Tidak ada tetangga yang valid ditemukan, stop.")
            break
        
        scored_neighbors = [(evaluate(neighbor, data), neighbor) for neighbor in neighbors]
        scored_neighbors.sort(key=lambda x: x[0])

        best_score, best_neighbor = scored_neighbors[0]
        print(f"Step {step+1}: Nilai fungsi objektif awal = {current_score}, akhir = {best_score}, Sideways Move = {side_count}")

        if best_score <= 0:
            print("[DONE] Solusi optimal ditemukan")
            current, current_score = best_neighbor, best_score
            break
        elif best_score < current_score:
            current, current_score = best_neighbor, best_score
            side_count = 0
        elif best_score == current_score and side_count < max_side:
            current, current_score = best_neighbor, best_score
            print("[SIDEWAYS] Melakukan sideways move")
            side_count += 1
        else:
            print("[DONE] Tidak ada perbaikan lebih lanjut, berhenti.")
            break
        visited.add(tuple(sorted(current.items())))

    return current, current_score

def hill_climbing_random_restart(state, data, slots, max_restarts=10, max_iter=1000):
    best_state = state
    best_score = evaluate(state, data)

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


        new_state, new_score = hill_climbing_sideways(initial_state, data, slots, max_iter=max_iter)
        if new_score < best_score:
            best_state, best_score = new_state, new_score

    return best_state, best_score

