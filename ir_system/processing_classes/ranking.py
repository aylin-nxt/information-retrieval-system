import math
import json

class RankHanlder:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    def process(self, query):
        processed_query = self.calculate_query_tf_weight(query)
        processed_query = self.get_query_idf_weight(processed_query)
        processed_query = self.calculate_tfidf_weight(processed_query)
        processed_query = self.query_length_normalization(processed_query)
        relevant_docs = self.get_terms_document(processed_query)
        rank_docs = self.rank_documents(processed_query, relevant_docs)
        docs_id = self.just_doc_id(rank_docs)
        print(rank_docs)
        return docs_id
        # with open('processed_query.json', "w") as json_file:
        #     json.dump(processed_query, json_file, indent=4)

    def just_doc_id(self, docs):
        docs_id = []
        for doc in docs:
            docs_id.append(doc[0])
        return docs_id

    def rank_documents(self, query_vector, relevant_docs):
        scores = {}

        for doc_id in relevant_docs:
            doc_score = 0.0
            for term, query_term_data in query_vector.items():
                if term in self.inverted_index and doc_id in self.inverted_index[term]["docs"]:
                    # Get normalized tf-idf for the term in document
                    doc_term_data = self.inverted_index[term]["docs"][doc_id]
                    doc_normalized_weight = doc_term_data["normalize-tf-idf"]
                    # Multiply with normalized query weight
                    doc_score += query_term_data["normalize-weight"] * doc_normalized_weight

            scores[doc_id] = doc_score

        # Sort by score descending
        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs

    @staticmethod
    def calculate_query_tf_weight(query):
        # store term with tf-weight
        query_weight = {}
        # create set of tokens
        query_set = set(query)
        # loop over terms
        for term in query_set:
            # get tf of term in query
            tf = query.count(term)
            # calculate tf-weight
            weight = 1+math.log(tf)
            # store tf and tf-weight in dict
            query_weight[term] = {
                "tf": tf,
                "tf-weight": weight
            }

        return query_weight

    def get_query_idf_weight(self, query):
        for term, value in query.items():
            if term in self.inverted_index.keys():
                idf = self.inverted_index[term]["idf"]
                query[term]['idf'] = idf
            else:
                query[term]['idf'] = 0
        return query

    @staticmethod
    def calculate_tfidf_weight(query):
        for term in query.keys():
            tfidf_weight = query[term]['idf'] * query[term]['tf-weight']
            query[term]['tfidf-weight'] = tfidf_weight
        return query

    @staticmethod
    def query_length_normalization(query):
        query_length_weights = 0
        for term in query.keys():
            query_length_weights += math.pow(query[term]["tfidf-weight"], 2)
        query_length_weights = math.sqrt(query_length_weights)

        for term in query.keys():
            query[term]['normalize-weight'] = query[term]["tfidf-weight"] / query_length_weights

        return query

    def get_terms_document(self, terms):
        docs_id = set()
        for term in terms.keys():
            # check term exists in inverted index
            if term in self.inverted_index:
                # get relevant docs of term
                term_docs = self.inverted_index[term]['docs']
                # get docs id
                docs_id = set(term_docs.keys())

        return docs_id