import json
import pandas as pd
from state import init_state, generate_slots, get_empty_slots, hari_list, jam_list
from objective import evaluate
from genetic_algorithm import genetic_algorithm
from hill_climbing import hill_climbing_sideways
# from debug import genetic_algorithm_debug


# ========================== PRINT TIME TABLE ==========================
def print_timetable(state, ruangan_list):
    print("\n==================== GENERATED TIMETABLE ====================")
    for ruang in ruangan_list:
        print(f"\nRuangan: {ruang}")
        print("-" * 60)

        table = {hari: [""] * len(jam_list) for hari in hari_list}

        for (hari, jam, ruang_slot), kode in state.items():
            if ruang_slot != ruang:
                continue
            if jam in jam_list:
                idx = jam_list.index(jam)
                table[hari][idx] = kode

        df_table = pd.DataFrame(table, index=jam_list)
        df_table.index.name = "Jam"
        print(df_table.fillna("").to_string())
        print("\n")

# ========================== MAIN ==========================
if __name__ == "__main__":
    with open("sample_input.json", "r") as input_file:
        data = json.load(input_file)

    kelas_mata_kuliah = data["kelas_mata_kuliah"]
    ruangan = [ruang["kode"] for ruang in data["ruangan"]]

    slots = generate_slots(ruangan)
    state = init_state(kelas_mata_kuliah, slots)

    print("[STATE REP] STATE AWAL:")
    df = pd.DataFrame(list(state.items()), columns=["key", "value"])
    print(df)

    print("\nEMPTY SLOTS:")
    empty_slots = get_empty_slots(state, slots)
    df_empty = pd.DataFrame(empty_slots, columns=["Hari", "Jam", "Ruangan"])
    print(df_empty.head(10))

    score = evaluate(state, data)
    print("\n[OBJ FUNCTION] EVALUATED SCORE:")
    print("Score total:", score)

    print("\n[START] Starting Genetic Algorithm...")
    # best_state, best_score, history = genetic_algorithm_debug(
    #     data, slots, pop_size=3, max_iter=100
    # )
    best_state, best_score, history = genetic_algorithm(
        data, slots, pop_size=3, max_iter=100, verbose=True
    )

    print("\n[RESULT] BEST STATE AFTER GENETIC ALGORITHM:")
    df_best = pd.DataFrame(list(best_state.items()), columns=["key", "value"])
    print(df_best)
    print("Best Score:", best_score)

    print_timetable(best_state, ruangan)
