import sys
import json
from pathlib import Path

# Add backend directory to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from app.guardrails.prompt_injection import PromptInjectionGuard


DATASET_PATH = (
    Path(__file__).parent
    / "datasets"
    / "prompt_injection_v1.json"
)


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    dataset = load_dataset()

    guard = PromptInjectionGuard()

    correct = 0

    for item in dataset:

        result = guard.check(item["text"])

        predicted = "safe" if result else "unsafe"
        expected = item["expected"]

        if predicted == expected:
            correct += 1

        print(
            f"ID {item['id']}: "
            f"expected={expected}, "
            f"predicted={predicted}"
        )

    accuracy = correct / len(dataset)

    print()
    print(f"Correct: {correct}/{len(dataset)}")
    print(f"Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    main()