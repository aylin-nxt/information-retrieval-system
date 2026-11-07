class SpellChecker:
    def __init__(self, set_token, inverted_index):
        self.words = set(set_token)
        self.inverted_index = inverted_index
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.stop_words = {
            # Articles
            "a", "an", "the",

            "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"

            # Basic pronouns
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
            "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",

            # Basic prepositions
            "about", "above", "across", "after", "against", "along", "among", "around", "at",
            "before", "behind", "below", "beneath", "beside", "between", "beyond", "by",
            "down", "during", "for", "from", "in", "into", "of", "off", "on", "onto", "over",
            "through", "to", "toward", "under", "up", "upon", "with", "within", "without",

            # Basic conjunctions
            "and", "but", "or", "nor", "so", "yet", "for", "although", "because", "since",
            "unless", "until", "when", "where", "while",

            # Common verbs (to be, to have, etc.)
            "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "having", "do", "does", "did", "doing", "will", "would", "shall", "should", "can",
            "could", "may", "might", "must",

            # Common adverbs
            "very", "really", "quite", "just", "only", "also", "too", "well", "much", "more",
            "most", "less", "least", "so", "such", "even", "still", "almost", "enough",
            "however", "therefore", "thus", "hence", "otherwise",

            # Common adjectives
            "all", "any", "both", "each", "every", "few", "many", "several", "some", "such",
            "no", "none", "other", "same", "different", "another",

            # Question words
            "what", "which", "who", "whom", "whose", "why", "how", "when", "where",

            # Demonstratives
            "this", "that", "these", "those",

            # Possessives
            "my", "your", "his", "her", "its", "our", "their",

            # Quantifiers
            "all", "any", "both", "each", "every", "few", "many", "much", "several", "some",
            "no", "none", "other", "same", "such", "another",

            # Miscellaneous common words
            "as", "if", "then", "than", "there", "here", "now", "then", "again", "once",
            "twice", "always", "never", "often", "sometimes", "usually", "just", "only",
            "even", "also", "too", "very", "really", "quite", "rather", "almost", "enough",
            "about", "above", "across", "after", "against", "along", "among", "around",
            "at", "before", "behind", "below", "beneath", "beside", "between", "beyond",
            "by", "down", "during", "for", "from", "in", "into", "of", "off", "on", "onto",
            "out", "over", "through", "to", "toward", "under", "up", "upon", "with",
            "within", "without",

            # Numbers (basic)
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "first", "second", "third", "last", "next", "previous",

            # Time-related
            "today", "tomorrow", "yesterday", "now", "then", "soon", "later", "early", "late",
            "time", "times", "year", "years", "month", "months", "week", "weeks", "day", "days",
            "hour", "hours", "minute", "minutes", "second", "seconds",

            # Basic greetings and polite words
            "hello", "hi", "hey", "please", "thank", "thanks", "sorry", "yes", "no", "ok", "okay",

            # Common contractions
            "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't", "haven't",
            "hasn't", "hadn't", "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot",
            "couldn't", "mustn't", "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
            "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd", "she'd", "we'd",
            "they'd", "i'll", "you'll", "he'll", "she'll", "we'll", "they'll",

        }

    def split(self, word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]

    def delete(self, word):
        return [a + b[1:] for a, b in self.split(word) if b]

    def replace(self, word):
        return [a + c + b[1:] for a, b in self.split(word) if b for c in self.alphabet]

    def insert(self, word):
        return [a + c + b for a, b in self.split(word) for c in self.alphabet]

    def edits1(self, word):
        return set(self.replace(word) + self.delete(word) + self.insert(word))

    def edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def known(self, words):
        return [w for w in words if w in self.words]

    def remove_stop_words(self, words):
        return [word for word in words if word not in self.stop_words]

    def get_term_idf(self, term):
        term_idf = 0
        # check term exists in inverted index
        if term in self.inverted_index:
            # get relevant docs of term
            term_idf = self.inverted_index[term]['idf']

        return term_idf

    def rank_by_idf(self, words):
        valid_words = []
        for word in words:
            try:
                idf = self.get_term_idf(word)
                print(word, idf)
                valid_words.append((word, idf))
            except KeyError:
                pass  # word not in inverted index → skip

        # Sort by IDF descending
        valid_words.sort(key=lambda x: x[1])
        return [w for w, _ in valid_words]

    def correct(self, word):
        """Correct a word by checking exact match, one-edit, then two-edit candidates."""
        # Exact match
        candidates = self.known([word])
        print("word: ", word)
        if candidates:
            return candidates

        # One-edit distance
        candidates = self.known(self.edits1(word))
        if candidates:
            print("one-edit: ")
            print("first: ",candidates)
            candidates = self.remove_stop_words(candidates)
            print("stop remove: ",candidates)
            candidates = self.rank_by_idf(candidates)
            print("idf sorted: ", candidates)
            return candidates

        # Two-edit distance
        candidates = self.known(self.edits2(word))
        if candidates:
            print("two-edit: ")
            print("first: ",candidates)
            candidates = self.remove_stop_words(candidates)
            print("stop remove: ",candidates)
            candidates = self.rank_by_idf(candidates)
            print("idf sorted: ", candidates)
            return candidates

        return []
