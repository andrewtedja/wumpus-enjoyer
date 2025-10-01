import json
from state import init_state
from objective import evaluate
import pandas as pd

if __name__ == "__main__":
    
    # ========================== Read Input (JSON) ==========================
    with open("data/sample_input.json", "r") as input_file:
        data = json.load(input_file)


    # ========================== State Representation ==========================

    kelas_mata_kuliah = data["kelas_mata_kuliah"]
    ruangan = [ruang["kode"] for ruang in data["ruangan"]]
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    jam_list = list(range(7, 16))

    state = init_state(kelas_mata_kuliah, ruangan, hari_list, jam_list)

    print("[STATE REP] STATE AWAL:")
    df = pd.DataFrame(list(state.items()), columns=["key", "value"])
    print(df)

    score = evaluate(state, data)

    

    print("\n[OBJ FUNCTION] EVALUATED SCORE: ")
    print("Score total:", score)
