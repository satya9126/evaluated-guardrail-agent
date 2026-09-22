from app.guardrails.output_guardrail import OutputGuardrail


def test_safe_output():
    guard = OutputGuardrail()

    result = guard.check(
        "Machine learning is a method that allows computers to learn from data."
    )

    assert result is True


def test_api_key_output():
    guard = OutputGuardrail()

    result = guard.check(
        "Your API key: sk-example123"
    )

    assert result is False


def test_password_output():
    guard = OutputGuardrail()

    result = guard.check(
        "Your password: secret123"
    )

    assert result is False