import json
import random
import pandas as pd
from typing import Dict

'''
> NOTES
- read input -> init state (kelas_mata_kuliah, waktu(jam), ruangan)
- state: dict {key: (hari, jam, ruangan), value: kelas}
'''

# ========================== Read Input (JSON) ==========================
# with open("data/sample_input.json", "r") as input_file:
#     data = json.load(input_file)


# # ========================== State Representation ==========================

# hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
# jam_list = list(range(7, 16))
# ruangan = [ruang["kode"] for ruang in data["ruangan"]]

# kelas_mata_kuliah = data["kelas_mata_kuliah"]



# ========================== INIT STATE ==========================
def init_state(kelas_mata_kuliah, ruangan, hari_list, jam_list) -> Dict:
    state = {}

    for matkul in kelas_mata_kuliah:
        kode= matkul["kode"]
        sks = matkul["sks"]

        hari = random.choice(hari_list)
        ruang = random.choice(ruangan)
        batas_awal = len(jam_list) - sks + 1
        jam_mulai = random.choice(jam_list[0:batas_awal])

        # iterate assign sesuai SKS (misalny 3 SKS = 3 jam berurutan)
        for shift in range(sks):
            state[(hari, jam_mulai + shift, ruang)] = kode
    return state


# ! TESTING
# if __name__ == "__main__":
#     state = init_state(kelas_mata_kuliah, ruangan)
#     print(state)
    

#     df = pd.DataFrame(list(state.items()), columns=["key", "value"])
#     print(df)
