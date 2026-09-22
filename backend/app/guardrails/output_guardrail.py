import re


class OutputGuardrail:

    def check(self, response: str) -> tuple[bool, str]:
        """
        Check whether the LLM response is safe to return.

        Returns:
            (True, response)  -> response is safe
            (False, message)  -> response should be blocked
        """

        # Check for possible system prompt leakage
        leakage_patterns = [
            "system prompt",
            "system message",
            "developer instructions",
            "hidden instructions",
            "internal instructions",
            "secret instructions",
        ]

        response_lower = response.lower()

        for pattern in leakage_patterns:
            if pattern in response_lower:
                return (
                    False,
                    "Response blocked because it may contain protected instructions."
                )

        # Check for common PII patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

        phone_pattern = r'\b\d{10}\b'

        if re.search(email_pattern, response):
            return (
                False,
                "Response blocked because it may contain personal information."
            )

        if re.search(phone_pattern, response):
            return (
                False,
                "Response blocked because it may contain personal information."
            )

        return True, response