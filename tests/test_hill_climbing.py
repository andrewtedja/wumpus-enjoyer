import json
import random
import unittest
from pathlib import Path

from src.hill_climbing import hill_climb_with_sideways
from src.objective import evaluate
from src.state import generate_slots, init_state


class HillClimbingTests(unittest.TestCase):
    def test_hill_climbing_never_worsens_objective(self) -> None:
        root_dir = Path(__file__).resolve().parents[1]

        with open(root_dir / "data" / "sample_input.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        slots = generate_slots([ruang["kode"] for ruang in data["ruangan"]])

        random.seed(0)
        initial_state = init_state(data["kelas_mata_kuliah"], slots)
        initial_score = evaluate(initial_state, data)

        result = hill_climb_with_sideways(
            initial_state,
            data,
            slots,
            max_iterations=200,
            max_sideways=20,
            random_seed=0,
        )

        final_score = evaluate(result.state, data)

        self.assertEqual(result.score, final_score)
        self.assertLessEqual(result.score, initial_score)


if __name__ == "__main__":
    unittest.main()
