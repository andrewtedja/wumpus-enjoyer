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
jam_list = list(range(7, 18))

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

        count = 0

        while count < sks:
            hari, jam_mulai, ruang = random.choice(slots)

            if (hari, jam_mulai, ruang) in used_slots:
                continue

            state[(hari, jam_mulai, ruang)] = kode
            used_slots.add((hari, jam_mulai, ruang))
            count += 1

    return state

# HELPER
def get_empty_slots(state, slots) -> List:
    return [slot for slot in slots if slot not in state.keys()]

