import re


class PIIDetector:

    def detect_and_redact(self, message: str) -> str:

        # Email addresses
        message = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
            '[EMAIL_REDACTED]',
            message
        )

        # Indian phone numbers
        message = re.sub(
            r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
            '[PHONE_REDACTED]',
            message
        )

        # Card-like numbers
        message = re.sub(
            r'(?<!\d)(?:\d{4}[-\s]?){3}\d{4}(?!\d)',
            '[CARD_REDACTED]',
            message
        )

        # IPv4 addresses
        message = re.sub(
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            '[IP_REDACTED]',
            message
        )

        return message