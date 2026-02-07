import re
from typing import List, Tuple


class NLPProcessor:
    def __init__(self):
        # Expanded stopwords
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
                "before",
                "after",
                "above",
                "below",
                "between",
                "under",
                "again",
                "further",
                "then",
                "once",
                "here",
                "there",
                "all",
                "both",
                "each",
                "few",
                "more",
                "most",
                "other",
                "some",
                "such",
                "only",
                "own",
                "same",
                "so",
                "than",
                "too",
                "very",
                "just",
                "now",
            ]
        )

        # Synonym mappings for better matching
        self.synonyms = {
            # Time related
            "timing": ["hours", "time", "schedule", "timings", "when"],
            "open": ["opens", "opening", "start", "starts", "available"],
            "close": ["closes", "closing", "end", "ends", "shut"],
            # Location related
            "where": ["location", "place", "find", "located"],
            "office": ["cell", "center", "centre", "section", "department"],
            # Network related
            "wifi": ["internet", "network", "connection", "online"],
            "password": ["passcode", "credentials", "login"],
            "access": ["connect", "login", "use", "get"],
            # Academic
            "exam": ["examination", "test", "assessment"],
            "course": ["subject", "class", "module"],
            "register": ["enroll", "enrol", "registration", "add"],
            "attendance": ["presence", "absent", "attend"],
            # Facilities
            "library": ["lib", "books", "reading room"],
            "hostel": ["dorm", "dormitory", "accommodation", "residence"],
            "mess": ["canteen", "dining", "cafeteria", "food"],
            "medical": ["health", "hospital", "clinic", "doctor"],
            # Documents
            "id": ["identity", "student card", "card"],
            "certificate": ["cert", "document", "proof"],
            # Actions
            "get": ["obtain", "take", "receive", "collect"],
            "apply": ["request", "submit", "file"],
            "contact": ["reach", "call", "email", "phone"],
            # Misc
            "timing": ["schedule", "time", "hours"],
            "fee": ["fees", "payment", "cost", "charge"],
            "curfew": ["gate", "closing", "entry"],
        }

        # Reverse synonym mapping for faster lookup
        self.synonym_map = {}
        for key, synonyms in self.synonyms.items():
            for synonym in synonyms:
                self.synonym_map[synonym] = key
            self.synonym_map[key] = key  # Map to itself too

    def detect_intent(self, message: str) -> str:
        """Detect what user wants to do - IMPROVED"""
        message_lower = message.lower()

        # Grievance keywords - expanded
        grievance_keywords = [
            "complaint",
            "grievance",
            "issue",
            "problem",
            "report",
            "submit complaint",
            "facing",
            "trouble",
            "not working",
            "broken",
            "complain",
            "file complaint",
            "register complaint",
            "damaged",
            "faulty",
            "error",
            "wrong",
            "incorrect",
            "missing",
            "lost",
        ]

        # FAQ indicators - expanded
        faq_keywords = [
            "what",
            "where",
            "when",
            "how",
            "who",
            "which",
            "whose",
            "tell me",
            "know",
            "find",
            "locate",
            "show",
            "give",
            "explain",
            "define",
            "describe",
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
            "sup",
            "yo",
            "greetings",
        ]

        # Check for grievance (stronger indicators)
        for keyword in grievance_keywords:
            if keyword in message_lower:
                return "grievance"

        # Check for greeting (must be at start)
        for keyword in greeting_keywords:
            if message_lower.strip().startswith(keyword):
                return "greeting"

        # Check for FAQ
        for keyword in faq_keywords:
            if keyword in message_lower:
                return "faq"

        # Default to FAQ (most questions don't start with what/where/etc)
        return "faq"

    def normalize_word(self, word: str) -> str:
        """Normalize word to its base synonym"""
        word = word.lower().strip()
        return self.synonym_map.get(word, word)

    def extract_keywords(self, text: str) -> List[str]:
        """Extract and normalize keywords - IMPROVED"""
        # Remove punctuation but keep spaces
        text = re.sub(r"[^\w\s]", "", text.lower())

        # Split into words
        words = text.split()

        # Remove stopwords and short words
        keywords = []
        for word in words:
            if word not in self.stop_words and len(word) > 2:
                # Normalize using synonyms
                normalized = self.normalize_word(word)
                keywords.append(normalized)

        return keywords

    def calculate_match_score(
        self, query: str, faq_question: str, faq_answer: str, faq_keywords: str
    ) -> float:
        """
        Calculate how well a FAQ matches the query - MUCH BETTER ALGORITHM
        Returns score from 0 to 100
        """
        query_keywords = set(self.extract_keywords(query))

        if not query_keywords:
            return 0

        score = 0

        # Extract keywords from each FAQ field
        question_keywords = set(self.extract_keywords(faq_question))
        answer_keywords = set(self.extract_keywords(faq_answer))
        db_keywords = set(self.extract_keywords(faq_keywords))

        # 1. EXACT MATCHES in question (highest weight)
        question_matches = query_keywords & question_keywords
        score += len(question_matches) * 15

        # 2. EXACT MATCHES in stored keywords (high weight)
        keyword_matches = query_keywords & db_keywords
        score += len(keyword_matches) * 10

        # 3. EXACT MATCHES in answer (medium weight)
        answer_matches = query_keywords & answer_keywords
        score += len(answer_matches) * 5

        # 4. PARTIAL MATCHES (substring matching)
        for q_word in query_keywords:
            # Check if query word is substring of FAQ words
            for faq_word in question_keywords:
                if q_word in faq_word or faq_word in q_word:
                    score += 3

            for faq_word in db_keywords:
                if q_word in faq_word or faq_word in q_word:
                    score += 2

        # 5. BONUS: Question type matching
        query_lower = query.lower()
        question_lower = faq_question.lower()

        # "What" questions
        if "what" in query_lower and "what" in question_lower:
            score += 5

        # "Where" questions
        if "where" in query_lower and "where" in question_lower:
            score += 5

        # "How" questions
        if "how" in query_lower and "how" in question_lower:
            score += 5

        # "When" questions (time-related)
        time_words = ["when", "time", "timing", "hour", "schedule"]
        if any(word in query_lower for word in time_words) and any(
            word in question_lower for word in time_words
        ):
            score += 5

        # 6. BONUS: Coverage (what percentage of query is matched)
        if query_keywords:
            coverage = len(question_matches | keyword_matches | answer_matches) / len(
                query_keywords
            )
            score += coverage * 10

        # 7. PENALTY: Length mismatch (very long FAQ for short query is suspicious)
        query_length = len(query_keywords)
        faq_length = len(question_keywords)
        if faq_length > query_length * 3:
            score *= 0.8

        return score

    def is_similar(self, word1: str, word2: str) -> bool:
        """Check if two words are similar (for fuzzy matching)"""
        # Normalize both
        w1 = self.normalize_word(word1)
        w2 = self.normalize_word(word2)

        # Exact match after normalization
        if w1 == w2:
            return True

        # Substring match
        if w1 in w2 or w2 in w1:
            return True

        # Check edit distance for typos (simple version)
        if len(w1) > 4 and len(w2) > 4:
            # Allow 1-2 character difference for longer words
            if abs(len(w1) - len(w2)) <= 2:
                differences = sum(c1 != c2 for c1, c2 in zip(w1, w2))
                if differences <= 2:
                    return True

        return False

    def extract_question_type(self, query: str) -> str:
        """Identify the type of question"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["what", "define", "meaning"]):
            return "what"
        elif any(word in query_lower for word in ["where", "location", "find"]):
            return "where"
        elif any(
            word in query_lower
            for word in ["when", "time", "timing", "schedule", "hour"]
        ):
            return "when"
        elif any(word in query_lower for word in ["how", "way", "method"]):
            return "how"
        elif any(word in query_lower for word in ["who", "whom"]):
            return "who"
        elif any(word in query_lower for word in ["which", "choose", "select"]):
            return "which"
        else:
            return "general"
