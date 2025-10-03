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

    for matkul in sorted(kelas_mata_kuliah, key = lambda x : -x["sks"]):
        kode = matkul["kode"]
        sks = matkul["sks"]

        attempt = 0
        valid = False
        while not valid and attempt < 1000:
            hari, jam_mulai, ruang = random.choice(slots)
            attempt += 1

            if jam_mulai + sks - 1 > max(jam_list):
                continue
            candidate_slots = [(hari, jam, ruang) for jam in range(jam_mulai, jam_mulai + sks)]
            if any(slot in used_slots for slot in candidate_slots):
                continue

            for slot in candidate_slots:
                state[slot] = kode
                used_slots.add(slot)
            valid = True
        if not valid:
            raise ValueError(f"Tidak dapat meng-assign {kode} dengan {sks} sks setelah {attempt} percobaan.")

            
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
