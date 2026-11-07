import re
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from ir_system.query_preprocessing.spell_correction import SpellChecker


class BooleanQueryPreprocessor:
    def __init__(self, set_tokens, inverted_index):
        self.nlp = spacy.load("en_core_web_sm")
        self.set_tokens = set_tokens
        self.inverted_index = inverted_index

    def processor(self, text):
        query = self.query_validation(text)
        print(query)
        query = self.handle_spell_checking(query)
        print(query)
        query = self.lemmatization(query)
        return query

    def handle_spell_checking(self, query):
        spellCorrectionObj = SpellChecker(self.set_tokens, self.inverted_index)
        corrected_query = []

        for word in query:
            # Don't spell-check boolean operators
            if word.upper() in {"AND", "OR", "NOT"}:
                corrected_query.append(word.upper())
                continue

            corrections = spellCorrectionObj.correct(word.lower())
            if corrections:
                corrected_query.append(corrections[0])  # pick best correction
            else:
                print("inja")
                corrected_query.append(word)  # keep original

        return corrected_query

    @staticmethod
    def query_validation(text):
        # char( => char (
        text = re.sub(r'(\S)\(', r'\1 (', text)
        # char) => char )
        text = re.sub(r'(\S)\)', r'\1 )', text)
        # (char => ( char
        text = re.sub(r'\((\S)', r'( \1', text)
        # )char => ) char
        text = re.sub(r'\)(\S)', r') \1', text)

        return list(text.split())

    def lemmatization(self, query):
        lemmatizer = WordNetLemmatizer()
        special = ["AND", "OR", "NOT", "(", ")"]
        # loop over tokens
        for index, token in enumerate(query):
            if token not in special:
                # get tag pos of token (noun, verb, adjective, adverb)
                term = self.nlp(token.lower())
                lemma = term[0].lemma_
                # update token
                query[index] = lemma

        return query

    # @staticmethod
    # def get_token_pos(token):
    #     if token.startswith('J'):
    #         return wordnet.ADJ
    #     elif token.startswith('V'):
    #         return wordnet.VERB
    #     elif token.startswith('N'):
    #         return wordnet.NOUN
    #     elif token.startswith('R'):
    #         return wordnet.ADV
    #     else:
    #         return wordnet.NOUN