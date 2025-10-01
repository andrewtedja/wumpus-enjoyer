import random
import pandas as pd
from typing import Dict, List

'''
> NOTES
- read input -> init state (kelas_mata_kuliah, waktu(jam), ruangan)
- state: dict {key: (hari, jam, ruangan), value: kelas}
'''

# ========================== State Representation ==========================
hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
jam_list = list(range(7, 16))

# ========================== Slot Definition ==========================
def generate_slots(ruangan):
    slots = []
    for hari in hari_list:
        for jam in jam_list:
            for ruang in ruangan:
                slots.append((hari, jam, ruang))
    return slots


# ========================== INIT STATE ==========================
def init_state(kelas_mata_kuliah, slots) -> Dict:
    state = {}
    used_slots = set()

    for matkul in kelas_mata_kuliah:
        kode = matkul["kode"]
        sks = matkul["sks"]

        valid = False
        while not valid:
            hari, jam_mulai, ruang = random.choice(slots)
            
            batas_awal = jam_mulai + sks - 1
            if batas_awal > 15:
                continue

            candidate_slots = [(hari, jam_mulai + offset, ruang) for offset in range(sks)]

            valid = True
            for cs in candidate_slots:
                if cs in used_slots:
                    valid = False
                    break

            if valid:
                for cs in candidate_slots:
                    state[cs] = kode
                    used_slots.add(cs)
            
    return state

# HELPER
def get_empty_slots(state, slots) -> List:
    return [slot for slot in slots if slot not in state.keys()]

# ! TESTING
# if __name__ == "__main__":
#     state = init_state(kelas_mata_kuliah, ruangan)
#     print(state)
    

#     df = pd.DataFrame(list(state.items()), columns=["key", "value"])
#     print(df)
