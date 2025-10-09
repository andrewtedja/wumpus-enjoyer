import copy
import random
from objective import evaluate

def getNeighbors(state, slots, kelas_mata_kuliah):
    neighbor_state = copy.deepcopy(state)
    dict_sks = {kelas["kode"]: kelas["sks"] for kelas in kelas_mata_kuliah}
    unique_classes = list(set(state.values()))
    rand_num = float(random.random())
    if rand_num < 0.5:
        # Shift kelas ke slot kosong
        kode_kelas = random.choice(unique_classes)
        slot_kode_kelas = [(hari, jam, ruang) for (hari, jam, ruang), kode in state.items() if kode == kode_kelas]
        slot_kosong = [slot for slot in slots if slot not in state]
        if not slot_kode_kelas:
            return None
        hari, jam, ruang = sorted(slot_kode_kelas)[0]
        sks = dict_sks[kode_kelas]
        posisi_lama = [(hari, jam + offset, ruang) for offset in range(sks)]
        for i in range(100):
            hari_baru, jam_baru, ruang_baru = random.choice(slot_kosong)
            if jam_baru + sks > 17:
                continue
            posisi_baru = [(hari_baru, jam_baru + offset, ruang_baru) for offset in range(sks)]
            if any(pos in state for pos in posisi_baru):
                continue # Posisi baru udah keisi
            for pos in posisi_lama:
                del neighbor_state[pos]
            for pos in posisi_baru:
                neighbor_state[pos] = kode_kelas
            return neighbor_state
    else:
        # Swap kelas antar dua slot
        if len(unique_classes) < 2:
            return None
        kelas1, kelas2 = random.sample(unique_classes, 2)
        slot_kelas1 = [slot for slot, kode in state.items() if kode == kelas1]
        slot_kelas2 = [slot for slot, kode in state.items() if kode == kelas2]
        if not slot_kelas1 or not slot_kelas2:
            return None
        
        for slot in slot_kelas1:
            neighbor_state[slot] = kelas2
        for slot in slot_kelas2:
            neighbor_state[slot] = kelas1

        return neighbor_state
    
    return None




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
                valid = True
                posisi_baru = []
                for offset in range(sks):
                    slot_baru = (hari, jam + offset, ruang)
                    if slot_baru in initial_state:
                        valid = False
                        break
                    posisi_baru.append(slot_baru)
                if valid:
                    for pos_baru in posisi_baru:
                        initial_state[pos_baru] = kode
                    placed = True
                    break

            if not placed:
                print(f"Gagal menempatkan kelas {kode} pada restart {restart+1}")
                break

        new_state, new_score = hill_climbing_sideways(initial_state, data, slots, max_iter=max_iter)
        if new_score < best_score:
            best_state, best_score = new_state, new_score

    return best_state, best_score

