import re
import spacy

from ir_system.query_preprocessing.spell_correction import SpellChecker


class ProximityQueryPreProcessor:
    def __init__(self, set_tokens, inverted_index):
        self.nlp = spacy.load("en_core_web_sm")
        self.set_tokens = set_tokens
        self.inverted_index = inverted_index

    def processor(self, query):
        query = self.tokenization(query)

        proximity = self.get_proximity(query)

        terms = self.handle_spell_checking(query)

        terms = self.lemmatization(terms)
        a = {
            "terms": terms,
            "proximity": proximity
        }
        print(a)
        # print({
        #     "terms": terms,
        #     "proximity": proximity
        # })
        return {
            "terms": terms,
            "proximity": proximity
        }

    def handle_spell_checking(self, query):
        print('nuhnuhu')
        spellCorrectionObj = SpellChecker(self.set_tokens, self.inverted_index)
        corrected_query = []
        reg = r'\/\d+'
        for word in query:
            if re.fullmatch(reg, word):
                continue

            corrections = spellCorrectionObj.correct(word.lower())
            if corrections:
                corrected_query.append(corrections[0])  # pick best correction
            else:
                print("inja")
                corrected_query.append(word)  # keep original

        return corrected_query

    @staticmethod
    def tokenization(query):
        return query.split()

    @staticmethod
    def get_proximity(query):
        proximity = []
        # proximity pattern </number>
        reg = r'\/\d+'
        index = 0
        while index < (len(query)-1):
            if not re.fullmatch(reg, query[index]) and not re.fullmatch(reg, query[index+1]):
                # distance between 2 word is one
                proximity.append(1)
                index += 1
            if not re.fullmatch(reg, query[index]) and re.fullmatch(reg, query[index+1]):
                # get distance from query
                proximity.append(int(query[index+1][-1]))
                index += 2

        return proximity

    def lemmatization(self, query):
        reg = r'\/\d+'
        terms = []
        for token in query:
            if not re.fullmatch(reg, token):
                # get tag pos of token (noun, verb, adjective, adverb)
                term = self.nlp(token.lower())
                lemma = term[0].lemma_
                # update token
                terms.append(lemma)

        return terms
