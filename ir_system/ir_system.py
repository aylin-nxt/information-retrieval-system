# query preprocessing
from .query_preprocessing.boolean_query_preprocessing import BooleanQueryPreprocessor
from .query_preprocessing.proximity_query_preprocessing import ProximityQueryPreProcessor
from .query_preprocessing.query_preprocessing import QueryPreProcessor
# document preprocessing
from .document_preprocessing.document_preprocessing import DocumentPreProcessor
# data structures
from .data_structures.inverted_index import InvertIndex
from .data_structures.positional_index import PositionalIndex
# indexing
from .processing_classes.boolean import BooleanHandling
from .processing_classes.permuterm import PermutermHandler
from .processing_classes.phrase import PhraseHandler
from .processing_classes.proximity import ProximityHandler
from .processing_classes.ranking import RankHanlder

import os

class IRSystem:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.folder = os.path.join(BASE_DIR, "ir_system", 'docs')
        # self.folder = os.path.join("ir_system", 'docs')

        documentPreProcessor = DocumentPreProcessor(self.folder)
        self.document = documentPreProcessor.process()
        self.set_tokens = documentPreProcessor.get_token_set()

        self.inverted_index = InvertIndex(self.document).initialize_inverted_index()
        self.positional_index = PositionalIndex(self.document).initialize_positional_index()

        self.query_preprocessor = QueryPreProcessor()

        self.boolean_query_preprocessor = BooleanQueryPreprocessor(self.set_tokens, self.inverted_index)
        self.boolean_handler = BooleanHandling(self.inverted_index)

        self.proximity_query_preprocessor = ProximityQueryPreProcessor(self.set_tokens, self.inverted_index)
        self.proximity_handler = ProximityHandler(self.positional_index)

        self.phrase_handler = PhraseHandler(self.positional_index)

        self.permuterm_handler = PermutermHandler(self.document ,self.inverted_index)

        self.rank_handler = RankHanlder(self.inverted_index)

    def boolean(self, query):
        query = self.boolean_query_preprocessor.processor(query)
        relevant_docs_id = self.boolean_handler.handle_query(query)
        relevant_docs = self.retrieve_documents(relevant_docs_id)
        return relevant_docs

    def phrase(self, query):
        query = self.query_preprocessor.processor(query)
        relevant_docs_id = self.phrase_handler.handle_query(query)
        relevant_docs = self.retrieve_documents(relevant_docs_id)
        return relevant_docs

    def proximity(self, query):
        query = self.proximity_query_preprocessor.processor(query)
        relevant_docs_id = self.proximity_handler.handle_query(query)
        relevant_docs = self.retrieve_documents(relevant_docs_id)
        return relevant_docs

    def wildcard(self, query):
        relevant_docs_id = self.permuterm_handler.process(query)
        relevant_docs = self.retrieve_documents(relevant_docs_id)
        return relevant_docs

    def rank(self, query):
        print(query)
        query = self.query_preprocessor.processor(query)
        relevant_docs_id = self.rank_handler.process(query)
        # print("relevant_docs_id", relevant_docs_id)
        relevant_docs = self.retrieve_documents(relevant_docs_id)
        # print("relevant_docs", relevant_docs)
        for doc in relevant_docs:
            print(doc[0:8])

        return relevant_docs

    def retrieve_documents(self, docs):
        documents = []
        filenames = os.listdir(self.folder)
        for index in docs:
            with open(os.path.join(self.folder, filenames[index]), 'r', encoding='utf-8') as f:
                # reading file
                text = f.read()
                # append to document list
                documents.append(text)
        return documents