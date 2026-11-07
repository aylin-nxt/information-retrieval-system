import re
import spacy
from nltk.corpus import stopwords

class QueryPreProcessor:
    def processor(self, text):
        query = self.case_folding(text)
        query = self.normalization(query)
        query = self.tokenization_lemmatization(query)
        # query = self.stopword_removal(query)
        return query

    @staticmethod
    def case_folding(query):
        # case folding raw text
        return query.lower()

    @staticmethod
    def normalization(query):
        # keeping words and numbers
        query = re.sub(r'[^a-z0-9\s]', " ", query)
        # return final result
        return query

    @staticmethod
    def tokenization_lemmatization(query):
        # load english language model
        nlp = spacy.load("en_core_web_sm")
        # tokenization each document
        tokens = nlp(query)
        # tokenization & limmatization query
        terms = [token.lemma_ for token in tokens if token.lemma_ and (token.is_alpha or token.like_num)]
        # return final result
        return terms

    @staticmethod
    def stopword_removal(query):
        stop_words = set(stopwords.words('english'))
        # remove stopword for query
        query = [token for token in query if token not in stop_words]
        # return final result
        return query