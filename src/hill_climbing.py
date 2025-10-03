import copy
import random
from objective import evaluate

def getNeighbors(state, slots, kelas_mata_kuliah, visited):
    neighbors = []

    dict_sks = {kelas["kode"]: kelas["sks"] for kelas in kelas_mata_kuliah}

    for (hari, jam, ruang), kode in state.items():
        sks = dict_sks.get(kode, 1)

        is_start = True
        for prev in range(1, sks):
            if (hari, jam - prev, ruang) in state:
                is_start = False
                break

        if not is_start:
            continue

        for (hariBaru, jamBaru, ruangBaru) in slots:
            valid = True
            posisi_baru = []
            for offset in range(sks):
                slot_baru = (hariBaru, jamBaru + offset, ruangBaru)
                if slot_baru in state:
                    valid = False
                    break
                posisi_baru.append(slot_baru)
            if valid:
                state_baru = copy.deepcopy(state)
                for offset in range(sks):
                    del state_baru[(hari, jam + offset, ruang)]
                for pos_baru in posisi_baru:
                    state_baru[pos_baru] = kode
                key = tuple(sorted(state_baru.items()))
                if key not in visited:
                    visited.add(key)
                    neighbors.append(state_baru)

    return neighbors

def hill_climbing_sideways(state, data, slots, max_iter=1000, max_side=500):
    current = state
    current_score = evaluate(current, data)
    side_count = 0
    visited = set()
    visited.add(tuple(sorted(current.items())))
    
    for step in range(max_iter):
        neighbors = getNeighbors(current, slots, data["kelas_mata_kuliah"], visited)
        if not neighbors:
            break
        
        scored_neighbors = [(evaluate(neighbor, data), neighbor) for neighbor in neighbors]
        scored_neighbors.sort(key=lambda x: x[0])

        best_score, best_neighbor = scored_neighbors[0]

        if best_score < current_score:
            current, current_score = best_neighbor, best_score
            side_count = 0
        elif best_score == current_score and side_count < max_side:
            current, current_score = best_neighbor, best_score
            side_count += 1
        else:
            break
        print(f"Step {step+1}: Nilai fungsi objektif = {current_score}, Sideway Move = {side_count}")

        return current, current_score

