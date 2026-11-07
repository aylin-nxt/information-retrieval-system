class PhraseHandler:
    def __init__(self, positional_index):
        self.positional_index = positional_index

    def handle_query(self, query):
        docs = self.get_relevant_docs(query)
        if not docs:
            return set()

        common_docs = self.get_common_docs(docs)
        if not common_docs:
            return set()

        # ChatGPT
        relevant_docs = self.check_phrase_match(query, common_docs, docs)

        return relevant_docs

    def get_relevant_docs(self, query):
        # get positions of terms
        docs = []
        # loop over each term
        for term in query:
            # check term exists in positional index
            if term in self.positional_index:
                # get relevant docs
                docs.append(self.positional_index[term])

        # relevant docs of each term
        return docs

    @staticmethod
    def get_common_docs(docs):
        # get common documents of terms
        common_docs = set(docs[0].keys())  # get relevant docs of first term
        for term_docs in docs[1:]:
            common_docs &= term_docs.keys()

        # relevant common documents based on terms
        return common_docs

    @staticmethod
    def check_phrase_match(query, common_docs, docs):
        matched_docs = set()

        for doc in common_docs:
            # Get positions for each term in the query in this document
            positions_lists = []
            for term in query:
                positions = docs[query.index(term)].get(doc, [])
                positions_lists.append(positions)

            # Use the positions of the first term as anchors
            first_term_positions = positions_lists[0]

            for pos in first_term_positions:
                match_found = True
                for i in range(1, len(query)):
                    expected_pos = pos + i
                    if expected_pos not in positions_lists[i]:
                        match_found = False
                        break
                if match_found:
                    matched_docs.add(doc)
                    break  # No need to keep checking this doc

        return matched_docs
