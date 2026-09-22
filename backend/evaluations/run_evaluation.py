import json
from pathlib import Path
from app.guardrails.prompt_injection import PromptInjectionGuard
from app.guardrails.pii_detector import PIIDetector
from app.guardrails.output_guardrail import OutputGuardrail
from app.guardrails.prompt_injection import PromptInjectionGuard
from evaluations.evaluation_dataset import (
    PROMPT_INJECTION_CASES,
    PII_CASES,
    OUTPUT_LEAKAGE_CASES,
    NORMAL_INPUT_CASES,
)

from evaluations.metrics import calculate_metrics


def evaluate_prompt_injection():
    guard = PromptInjectionGuard()

    correct = 0

    for case in PROMPT_INJECTION_CASES:
        result = guard.check(case["input"])

        if result == case["expected"]:
            correct += 1

    return correct, len(PROMPT_INJECTION_CASES)


def evaluate_pii():
    detector = PIIDetector()

    correct = 0

    for case in PII_CASES:
        result = detector.detect_and_redact(case["input"])

        if case["expected"] in result and case["input"] != result:
            correct += 1

    return correct, len(PII_CASES)


def evaluate_output_guardrail():
    guard = OutputGuardrail()

    correct = 0

    for case in OUTPUT_LEAKAGE_CASES:
        allowed, _ = guard.check(case["input"])

        if allowed == case["expected"]:
            correct += 1

    return correct, len(OUTPUT_LEAKAGE_CASES)


def evaluate_normal_inputs():
    guard = PromptInjectionGuard()

    correct = 0

    for case in NORMAL_INPUT_CASES:
        result = guard.check(case["input"])

        if result == case["expected"]:
            correct += 1

    return correct, len(NORMAL_INPUT_CASES)


def main():
    injection_correct, injection_total = evaluate_prompt_injection()

    pii_correct, pii_total = evaluate_pii()

    leakage_correct, leakage_total = evaluate_output_guardrail()

    normal_correct, normal_total = evaluate_normal_inputs()

    metrics = calculate_metrics(
        injection_blocked=injection_correct,
        injection_total=injection_total,
        pii_redacted=pii_correct,
        pii_total=pii_total,
        leakage_blocked=leakage_correct,
        leakage_total=leakage_total,
        normal_allowed=normal_correct,
        normal_total=normal_total,
    )
    results = {
        "prompt_injection_block_rate": metrics["prompt_injection_block_rate"],
        "pii_redaction_rate": metrics["pii_redaction_rate"],
        "output_leakage_block_rate": metrics["output_leakage_block_rate"],
        "normal_request_pass_rate": metrics["normal_request_pass_rate"],
        "false_positive_rate": metrics["false_positive_rate"],
    }

    results_path = Path(__file__).parent / "results.json"

    with open(results_path, "w") as file:
        json.dump(results, file, indent=4)

    print("\n========== EVALUATION RESULTS ==========")

    print(
        f"Prompt Injection Block Rate: "
        f"{metrics['prompt_injection_block_rate']:.2f}%"
    )

    print(
        f"PII Redaction Rate: "
        f"{metrics['pii_redaction_rate']:.2f}%"
    )

    print(
        f"Output Leakage Block Rate: "
        f"{metrics['output_leakage_block_rate']:.2f}%"
    )

    print(
        f"Normal Request Pass Rate: "
        f"{metrics['normal_request_pass_rate']:.2f}%"
    )

    print(
        f"False Positive Rate: "
        f"{metrics['false_positive_rate']:.2f}%"
    )

    print("========================================\n")


if __name__ == "__main__":
    main()