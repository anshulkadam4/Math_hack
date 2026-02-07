import re


class NLPProcessor:
    def __init__(self):
        # Common English stopwords
        self.stop_words = set(
            [
                "the",
                "is",
                "at",
                "which",
                "on",
                "a",
                "an",
                "and",
                "or",
                "but",
                "in",
                "with",
                "to",
                "for",
                "of",
                "as",
                "by",
                "this",
                "that",
                "are",
                "was",
                "were",
                "been",
                "be",
                "have",
                "has",
                "had",
                "do",
                "does",
                "did",
                "will",
                "would",
                "should",
                "could",
                "may",
                "might",
                "can",
                "about",
                "from",
                "into",
                "through",
                "during",
            ]
        )

    def detect_intent(self, message):
        """Detect what user wants to do"""
        message_lower = message.lower()

        # Grievance keywords
        grievance_keywords = [
            "complaint",
            "grievance",
            "issue",
            "problem",
            "report",
            "submit",
            "facing",
            "trouble",
            "not working",
            "broken",
            "complain",
            "file complaint",
            "register complaint",
        ]

        # FAQ keywords
        faq_keywords = [
            "what",
            "where",
            "when",
            "how",
            "who",
            "which",
            "tell me",
            "know",
            "find",
            "locate",
            "?",
        ]

        # Greeting keywords
        greeting_keywords = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good evening",
            "good afternoon",
            "start",
            "help",
            "hola",
            "namaste",
        ]

        # Check for grievance intent
        if any(word in message_lower for word in grievance_keywords):
            return "grievance"

        # Check for greeting
        elif any(message_lower.startswith(word) for word in greeting_keywords):
            return "greeting"

        # Check for FAQ
        elif any(word in message_lower for word in faq_keywords):
            return "faq"

        # Default to FAQ search
        else:
            return "faq"

    def extract_keywords(self, text):
        """Extract important keywords from text"""
        # Remove punctuation and convert to lowercase
        text = re.sub(r"[^\w\s]", "", text.lower())

        # Split into words
        words = text.split()

        # Remove stop words and short words
        keywords = [
            word for word in words if word not in self.stop_words and len(word) > 2
        ]

        return " ".join(keywords)

    def calculate_similarity(self, text1, text2):
        """Simple keyword overlap similarity"""
        words1 = set(self.extract_keywords(text1).split())
        words2 = set(self.extract_keywords(text2).split())

        if not words1 or not words2:
            return 0

        overlap = len(words1 & words2)
        total = len(words1 | words2)

        return overlap / total if total > 0 else 0
