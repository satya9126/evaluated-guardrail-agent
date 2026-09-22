from app.guardrails.pii_detector import PIIDetector


def test_email_redaction():
    detector = PIIDetector()

    result = detector.detect_and_redact(
        "My email is satya@example.com"
    )

    assert "[EMAIL_REDACTED]" in result
    assert "satya@example.com" not in result


def test_phone_redaction():
    detector = PIIDetector()

    result = detector.detect_and_redact(
        "My phone number is 9876543210"
    )

    assert "[PHONE_REDACTED]" in result
    assert "9876543210" not in result


def test_card_redaction():
    detector = PIIDetector()

    result = detector.detect_and_redact(
        "My card number is 1234 5678 9012 3456"
    )

    assert "[CARD_REDACTED]" in result
    assert "1234 5678 9012 3456" not in result


def test_ip_redaction():
    detector = PIIDetector()

    result = detector.detect_and_redact(
        "The server IP is 192.168.1.10"
    )

    assert "[IP_REDACTED]" in result
    assert "192.168.1.10" not in result