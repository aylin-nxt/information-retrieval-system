import math
import json

class InvertIndex:
    def __init__(self, docs):
        self.docs = docs


    def initialize_inverted_index(self):
        # creating set of tokens
        tokens_set = self.creating_tokens_set(self.docs)
        # creating inverted index with tf
        inverted_index = self.inverted_index_with_tf(tokens_set, self.docs)
        with open('inverted_index1.json', "w") as json_file:
            json.dump(inverted_index, json_file, indent=4)

        # adding df, idf to inverted index
        inverted_index = self.adding_df_idf(inverted_index)
        with open('inverted_index2.json', "w") as json_file:
            json.dump(inverted_index, json_file, indent=4)

        # adding tf-idf weighting to inverted index
        inverted_index = self.adding_tfidf_weight(inverted_index)
        with open('inverted_index3.json', "w") as json_file:
            json.dump(inverted_index, json_file, indent=4)

        #  document length normalization
        documents_length = self.calculate_document_length(inverted_index)
        with open('inverted_index4.json', "w") as json_file:
            json.dump(inverted_index, json_file, indent=4)

        # store normalize weight in inverted index
        inverted_index = self.implement_length_normalization(inverted_index, documents_length)
        with open('inverted_index5.json', "w") as json_file:
            json.dump(inverted_index, json_file, indent=4)

        # final inverted index
        return inverted_index

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
    def inverted_index_with_tf(tokens_set, docs):
        # initialize inverted index dictionary
        inverted_index = {}
        # loop over token set
        for token in tokens_set:
            # insert token as term in inverted index
            inverted_index[token] = {"docs": {}}
            # loop over document's tokens
            for docId, doc_tokens in docs.items():
                # checking which document have the term
                if token in doc_tokens:
                    # calculate how many occurrence of term in document (tf: term frequency)
                    tf = doc_tokens.count(token)
                    # calculate the tf weight
                    tf_weight = 1 + math.log(tf)
                    # store tf and tf-weight
                    item = {
                        "tf": tf,
                        "tf_weight": tf_weight
                    }
                    # store tf, tf-weight in inverted index
                    inverted_index[token]['docs'][docId] = item
        # return inverted index
        return inverted_index

    @staticmethod
    def adding_df_idf(inverted_index):
        # loop over terms in inverted index
        for term, value in inverted_index.items():
            # calculating df of term
            df = len(value['docs'])  # get the number of document that term exists in it
            # store df of term in inverted index
            inverted_index[term]['df'] = df
            # calculating idf of term
            idf = math.log(30 / df)
            # store idf of the term in inverted index
            inverted_index[term]["idf"] = idf

        # return updated inverted index
        return inverted_index

    @staticmethod
    def adding_tfidf_weight(inverted_index):
        # loop over inverted index to get term
        for term, value in inverted_index.items():
            # getting idf for calculation of the tf-idf weight
            idf_weight = value['idf']
            # loop over documents that term exists on them
            for doc, docValue in inverted_index[term]['docs'].items():
                # getting tf-weight to calculation of the tf-idf weight
                tf_weight = docValue['tf_weight']
                # calculating tf-idf weight and store it in inverted index
                inverted_index[term]['docs'][doc]['tf-idf'] = tf_weight * idf_weight

        # return updated inverted index
        return inverted_index

    @staticmethod
    def calculate_document_length(inverted_index):
        docs_weight = {}
        # loop over terms
        for term, value in inverted_index.items():
            # loop over documents
            for doc_id, doc_value in value['docs'].items():
                # initialize the weight of document
                if doc_id not in docs_weight:
                    docs_weight[doc_id] = 0
                # add weight of document's term
                docs_weight[doc_id] += math.pow(doc_value['tf-idf'], 2)

        # find root of weight
        for doc, weight in docs_weight.items():
            docs_weight[doc] = math.sqrt(weight)

        # return length of the documents
        return docs_weight

    @staticmethod
    def implement_length_normalization(inverted_index, documents_length):
        # loop over inverted index to get term
        for term, value in inverted_index.items():
            # loop over documents that term exists on them
            for doc, docValue in inverted_index[term]['docs'].items():
                # getting tf_idf to calculation of the tf-idf normalized weight
                tf_idf = docValue['tf-idf']
                # calculating tf-idf weight and store it in inverted index
                inverted_index[term]['docs'][doc]['normalize-tf-idf'] = tf_idf / documents_length[doc]

        # return updated inverted index
        return inverted_index
