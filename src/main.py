import json
from state import init_state, generate_slots, get_empty_slots
from objective import evaluate
from hill_climbing import hill_climbing_sideways, hill_climbing_random_restart
import pandas as pd

if __name__ == "__main__":
    
    # ========================== Read Input (JSON) ==========================
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
    print(df_empty.head(20))

    score = evaluate(state, data)

    print("\n[OBJ FUNCTION] EVALUATED SCORE: ")
    print("Score total:", score)

    print("\n[ALGORITHM] Pilihan Algoritma:")
    print("1. Hill Climbing with Sideways Move")
    print("2. Hill Climbing with Random Restart")

    n : int = int(input("\nMasukkan pilihan algoritma: "))

    if n == 1:
        print("\n[START] Starting Hill Climbing with Sideways Move...")
        best_state, best_score = hill_climbing_sideways(state, data, slots, max_iter=1000, max_side=500)
        print("\n[RESULT] BEST STATE AFTER HILL CLIMBING WITH SIDEWAYS MOVE:")
        df_best = pd.DataFrame(list(best_state.items()), columns=["key", "value"])
        print(df_best)
        print("Best Score:", best_score)
    elif n == 2:
        print("\n[START] Starting Hill Climbing with Random Restart...")
        best_state, best_score = hill_climbing_random_restart(state, data, slots, max_restarts=10, max_iter=1000)
        print("\n[RESULT] BEST STATE AFTER HILL CLIMBING WITH RANDOM RESTART:")
        df_best = pd.DataFrame(list(best_state.items()), columns=["key", "value"])
        print(df_best)
        print("Best Score:", best_score)
    else:
        print("Pilihan tidak valid.")