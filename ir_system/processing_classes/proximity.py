from itertools import product

class ProximityHandler:
    def __init__(self, positional_index):
        self.positional_index = positional_index

    def handle_query(self, query):
        docs = self.get_relevant_docs(query['terms'])
        if not docs:
            return set()

        common_docs = self.get_common_docs(docs)
        if not common_docs:
            return set()

        # ChatGPT
        relevant_docs = self.get_matching_documents(query, common_docs, docs)

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
        print("docs: ", docs)
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
    def get_matching_documents(query, common_docs, docs):
        # print(query)
        # print(common_docs)
        # print(docs)
        terms = query['terms']
        proximities = query['proximity']
        matched_docs = set()

        for doc in common_docs:
            # Get positions for each term in this document
            positions_lists = []
            for i in range(len(terms)):
                positions = docs[i].get(doc, [])
                positions_lists.append(positions)

            # Try all combinations of one position per term
            for combo in product(*positions_lists):
                # Must be strictly increasing (ordered terms)
                if not all(combo[i] < combo[i + 1] for i in range(len(combo) - 1)):
                    continue

                # Check proximity distances
                valid = True
                for i in range(len(proximities)):
                    expected_distance = proximities[i]
                    actual_distance = combo[i + 1] - combo[i]
                    if actual_distance > expected_distance:
                        valid = False
                        break

                if valid:
                    matched_docs.add(doc)
                    break  # No need to check more combos for this doc

        return matched_docs