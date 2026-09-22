def calculate_rate(successes: int, total: int) -> float:
    if total == 0:
        return 0.0

    return (successes / total) * 100


def calculate_false_positive_rate(
    blocked_normal_requests: int,
    normal_requests: int,
) -> float:
    if normal_requests == 0:
        return 0.0

    return (blocked_normal_requests / normal_requests) * 100


def calculate_metrics(
    injection_blocked: int,
    injection_total: int,
    pii_redacted: int,
    pii_total: int,
    leakage_blocked: int,
    leakage_total: int,
    normal_allowed: int,
    normal_total: int,
):
    normal_pass_rate = calculate_rate(
        normal_allowed,
        normal_total
    )

    blocked_normal_requests = normal_total - normal_allowed

    false_positive_rate = calculate_false_positive_rate(
        blocked_normal_requests,
        normal_total
    )

    return {
        "prompt_injection_block_rate": calculate_rate(
            injection_blocked,
            injection_total
        ),
        "pii_redaction_rate": calculate_rate(
            pii_redacted,
            pii_total
        ),
        "output_leakage_block_rate": calculate_rate(
            leakage_blocked,
            leakage_total
        ),
        "normal_request_pass_rate": normal_pass_rate,
        "false_positive_rate": false_positive_rate,
    }