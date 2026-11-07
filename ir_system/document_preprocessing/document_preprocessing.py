import os
import re
import spacy
from nltk.corpus import stopwords

class DocumentPreProcessor:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.set_tokens = []

    def process(self):
        docs = self.load_documents(self.folder_name)
        docs = self.case_folding(docs)
        docs = self.normalization(docs)
        docs = self.tokenization_lemmatization(docs)
        self.set_tokens = self.creating_tokens_set(docs)
        return docs


    def get_token_set(self):
        return self.set_tokens

    def creating_tokens_set(self, docs):
        # initialize token set
        tokens_set = set()

        for docId, tokens in docs.items():
            tokens_set.update(tokens)

        # tokens_set = self.stopword_removal(tokens_set)
        return tokens_set

    @staticmethod
    def load_documents(folder_name):
        docs = []
        # get name of the files in directory
        for filename in os.listdir(folder_name):
            # read each file
            with open(os.path.join(folder_name, filename), 'r', encoding='utf-8') as f:
                # reading file
                text = f.read()
                # append to document list
                docs.append(text)
        # return all docs
        return docs

    @staticmethod
    def case_folding(docs):
        lowercase_docs = []
        # loop over for each document
        for doc in docs:
            # case folding the document
            doc = doc.lower()
            # append to list of case folded documents
            lowercase_docs.append(doc)
        # return final result
        return lowercase_docs

    @staticmethod
    def normalization(docs):
        normalized_docs = []
        # loop over documents
        for doc in docs:
            # remove <[number]> from documents (wikipedia format)
            doc = re.sub(r'\[\d+\]', '', doc)
            # keeping words and numbers
            doc = re.sub(r'(\d+).(\d+)', r'\1', doc)
            doc = re.sub(r'(\d+),(\d+)', r'\1\2', doc)
            # keeping words and numbers
            doc = re.sub(r'[^a-z0-9\%\s]', " ", doc)
            # append to list of normalized docs
            normalized_docs.append(doc)
        # return final result
        return normalized_docs

    @staticmethod
    def tokenization_lemmatization(docs):
        documents = {}
        # load english language model
        nlp = spacy.load("en_core_web_sm")
        # loop over documents
        for index, doc in enumerate(docs):
            # tokenization each document
            tokens = nlp(doc)
            # save lemma of tokens for each document
            documents[index] = [token.lemma_ for token in tokens if token.lemma_ and (token.is_alpha or token.like_num)]
        # return final result
        return documents

    # @staticmethod
    # def stopword_removal(set_tokens):
    #     # stop_words = set(stopwords.words('english'))
    #     stop_words = [
    #         # Articles
    #         "a", "an", "the",
    #
    #         "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    #         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    #
    #         # Basic pronouns
    #         "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    #         "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    #         "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    #
    #         # Basic prepositions
    #         "about", "above", "across", "after", "against", "along", "among", "around", "at",
    #         "before", "behind", "below", "beneath", "beside", "between", "beyond", "by",
    #         "down", "during", "for", "from", "in", "into", "of", "off", "on", "onto", "over",
    #         "through", "to", "toward", "under", "up", "upon", "with", "within", "without",
    #
    #         # Basic conjunctions
    #         "and", "but", "or", "nor", "so", "yet", "for", "although", "because", "since",
    #         "unless", "until", "when", "where", "while",
    #
    #         # Common verbs (to be, to have, etc.)
    #         "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    #         "having", "do", "does", "did", "doing", "will", "would", "shall", "should", "can",
    #         "could", "may", "might", "must",
    #
    #         # Common adverbs
    #         "very", "really", "quite", "just", "only", "also", "too", "well", "much", "more",
    #         "most", "less", "least", "so", "such", "even", "still", "almost", "enough",
    #         "however", "therefore", "thus", "hence", "otherwise",
    #
    #         # Common adjectives
    #         "all", "any", "both", "each", "every", "few", "many", "several", "some", "such",
    #         "no", "none", "other", "same", "different", "another",
    #
    #         # Question words
    #         "what", "which", "who", "whom", "whose", "why", "how", "when", "where",
    #
    #         # Demonstratives
    #         "this", "that", "these", "those",
    #
    #         # Possessives
    #         "my", "your", "his", "her", "its", "our", "their",
    #
    #         # Quantifiers
    #         "all", "any", "both", "each", "every", "few", "many", "much", "several", "some",
    #         "no", "none", "other", "same", "such", "another",
    #
    #         # Miscellaneous common words
    #         "as", "if", "then", "than", "there", "here", "now", "then", "again", "once",
    #         "twice", "always", "never", "often", "sometimes", "usually", "just", "only",
    #         "even", "also", "too", "very", "really", "quite", "rather", "almost", "enough",
    #         "about", "above", "across", "after", "against", "along", "among", "around",
    #         "at", "before", "behind", "below", "beneath", "beside", "between", "beyond",
    #         "by", "down", "during", "for", "from", "in", "into", "of", "off", "on", "onto",
    #         "out", "over", "through", "to", "toward", "under", "up", "upon", "with",
    #         "within", "without",
    #
    #         # Numbers (basic)
    #         "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    #         "first", "second", "third", "last", "next", "previous",
    #
    #         # Time-related
    #         "today", "tomorrow", "yesterday", "now", "then", "soon", "later", "early", "late",
    #         "time", "times", "year", "years", "month", "months", "week", "weeks", "day", "days",
    #         "hour", "hours", "minute", "minutes", "second", "seconds",
    #
    #         # Basic greetings and polite words
    #         "hello", "hi", "hey", "please", "thank", "thanks", "sorry", "yes", "no", "ok", "okay",
    #
    #         # Common contractions
    #         "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't", "haven't",
    #         "hasn't", "hadn't", "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot",
    #         "couldn't", "mustn't", "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
    #         "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd", "she'd", "we'd",
    #         "they'd", "i'll", "you'll", "he'll", "she'll", "we'll", "they'll",
    #
    #     ]
    #     # loop over documents
    #     final_tokens = set()
    #     for token in set_tokens:
    #         # remove stopword for each document
    #         if token not in stop_words:
    #             final_tokens.add(token)
    #
    #     # return final result
    #     return final_tokens