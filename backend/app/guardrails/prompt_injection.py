import re


class PromptInjectionGuard:

    def check(self, message: str) -> bool:

        message_lower = message.lower()

        suspicious_patterns = [

            # Instruction override

            r"ignore\s+(all\s+)?previous\s+instructions?",
            r"disregard\s+(all\s+)?previous\s+instructions?",
            r"forget\s+(all\s+)?previous\s+instructions?",
            r"forget\s+your\s+instructions?",
            r"ignore\s+everything\s+you\s+were\s+told",
            r"disregard\s+everything\s+you\s+were\s+told",

            # System prompt extraction
            r"reveal\s+(your\s+)?system\s+prompt",
            r"show\s+(me\s+)?(your\s+)?system\s+prompt",
            r"tell\s+me\s+(your\s+)?system\s+prompt",
            r"expose\s+(your\s+)?hidden\s+instructions?",
            r"reveal\s+(your\s+)?hidden\s+instructions?",
            r"show\s+(me\s+)?(your\s+)?hidden\s+instructions?",

            # Instruction extraction
            r"reveal\s+the\s+instructions?\s+(that|given)",
            r"show\s+the\s+instructions?\s+(that|were|given)",
            r"tell\s+me\s+the\s+instructions?\s+(that|were|given)",

            # Override / manipulation
            r"override\s+(your\s+)?previous\s+rules?",
            r"override\s+(your\s+)?instructions?",
            r"follow\s+only\s+my\s+instructions?",
            r"follow\s+my\s+instructions?\s+instead",

            # System message / secret extraction
            r"reveal\s+(your\s+)?secret\s+(system\s+)?message",
            r"show\s+(me\s+)?(your\s+)?secret\s+(system\s+)?message",
            r"tell\s+me\s+(your\s+)?hidden\s+message",
        ]

        for pattern in suspicious_patterns:

            if re.search(pattern, message_lower):

                return False

        return True