import sys
import json
from pathlib import Path

# Add backend directory to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from app.services.security_classifier import SecurityClassifier


DATASET_PATH = (
    Path(__file__).parent
    / "datasets"
    / "prompt_injection_v2.json"
)


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    dataset = load_dataset()
    classifier = SecurityClassifier()

    correct = 0

    # Confusion matrix values
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for item in dataset:

        is_attack = classifier.is_prompt_injection(
            item["text"]
        )

        predicted = "unsafe" if is_attack else "safe"
        expected = item["expected"]

        # Count correct predictions
        if predicted == expected:
            correct += 1

        # Confusion matrix
        if expected == "unsafe" and predicted == "unsafe":
            true_positive += 1

        elif expected == "safe" and predicted == "safe":
            true_negative += 1

        elif expected == "safe" and predicted == "unsafe":
            false_positive += 1

        elif expected == "unsafe" and predicted == "safe":
            false_negative += 1

        print(
            f"ID {item['id']}: "
            f"expected={expected}, "
            f"predicted={predicted}"
        )

    total = len(dataset)

    accuracy = correct / total if total else 0

    precision = (
        true_positive /
        (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else 0
    )

    recall = (
        true_positive /
        (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else 0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    false_positive_rate = (
        false_positive /
        (false_positive + true_negative)
        if (false_positive + true_negative) > 0
        else 0
    )

    false_negative_rate = (
        false_negative /
        (false_negative + true_positive)
        if (false_negative + true_positive) > 0
        else 0
    )

    print()
    print("=" * 45)
    print("AI SECURITY EVALUATION")
    print("=" * 45)

    print(f"Total Cases:        {total}")
    print(f"Correct:             {correct}")
    print(f"Incorrect:           {total - correct}")

    print()
    print("CONFUSION MATRIX")
    print("-" * 45)
    print(f"True Positives:     {true_positive}")
    print(f"True Negatives:     {true_negative}")
    print(f"False Positives:    {false_positive}")
    print(f"False Negatives:    {false_negative}")

    print()
    print("METRICS")
    print("-" * 45)
    print(f"Accuracy:           {accuracy:.2%}")
    print(f"Precision:          {precision:.2%}")
    print(f"Recall:             {recall:.2%}")
    print(f"F1 Score:           {f1:.2%}")

    print()
    print("ERROR RATES")
    print("-" * 45)
    print(f"False Positive Rate: {false_positive_rate:.2%}")
    print(f"False Negative Rate: {false_negative_rate:.2%}")

    print("=" * 45)


if __name__ == "__main__":
    main()