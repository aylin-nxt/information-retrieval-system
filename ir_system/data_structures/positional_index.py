from ..utils.funcs import getIndex
import json



class PositionalIndex:
    def __init__(self, docs):
        self.docs = docs

    def initialize_positional_index(self):
        # creating set of tokens
        tokens_set = self.creating_tokens_set(self.docs)
        # creating positional index
        positional_index = self.creating_positional_index(tokens_set, self.docs)
        with open('positional_index.json', "w") as json_file:
            json.dump(positional_index, json_file, indent=4)
        # final positional index
        return positional_index

    @staticmethod
    def creating_tokens_set(docs):
        # initialize token set
        tokens_set = set()
        # add each token of documents to one set
        for docId, tokens in docs.items():
            tokens_set.update(tokens)
        # return final result( set of tokens )
        return tokens_set

    @staticmethod
    def creating_positional_index(tokens_set, docs):
        positional_index = {}
        # loop over token
        for token in tokens_set:
            # initialize term in positional index
            positional_index[token] = {}
            # loop over documents for get positional of each term
            for docId, doc_tokens in docs.items():
                # get index of token that appeared in document
                indexes = getIndex(doc_tokens, token)
                # check term appeared in document
                if len(indexes):
                    # save positions of term
                    positional_index[token][docId] = indexes

        return positional_index