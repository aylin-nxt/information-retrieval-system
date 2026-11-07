from ..data_structures.Trie import Trie

class PermutermHandler:
    def __init__(self, docs, inverted_index):
        self.trie = Trie(docs)
        self.inverted_index = inverted_index

    def process(self, query):
        # get permuterm form on query
        permuterm = self.permuterm_form(query.lower())
        # get valid terms
        trie_terms = self.trie.starts_with(permuterm)
        print(trie_terms)
        # turn into valid form of term
        valid_terms = self.valid_trie_terms(trie_terms)
        # get documents that terms appeared on them
        documents = self.get_terms_document(valid_terms)
        return documents

    @staticmethod
    def permuterm_form(query):
        # add $ to end of query
        query += "$"
        # add split into 2 section
        prefix, suffix = query.split("*")
        # permuterm form
        permuterm = suffix + prefix
        return permuterm

    @staticmethod
    def valid_trie_terms(trie_terms):
        valid_terms = []
        for term in trie_terms:
            prefix, suffix = term.split("$")
            valid_term = suffix + prefix
            valid_terms.append(valid_term)
        return valid_terms

    def get_terms_document(self, terms):
        docs_id = set()
        # check term exists in inverted index
        for term in terms:
            if term in self.inverted_index:
                # get relevant docs of term
                term_docs = self.inverted_index[term]['docs']
                # get docs id
                docs_id.update(term_docs.keys())

        return docs_id