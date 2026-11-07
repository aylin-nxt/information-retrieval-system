class BooleanHandling:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        self.all_docs = set(range(21))

    def handle_query(self, query):
        posting_list = self.get_posting_list(query)
        postfix = self.create_postfix(query)
        result = self.evaluate_postfix(postfix, posting_list, self.all_docs)
        return result

    def get_posting_list(self, query):
        specials = ["AND", "NOT", "OR", "(", ")"]
        # get docs that tokens appeared on them
        posting_list = {}
        for term in query:
            if term not in specials:
                # get relevant docs id of term
                docs_id = self.get_term_document(term)
                # save in posting list
                posting_list[term] = docs_id

        return posting_list

    def get_term_document(self, term):
        docs_id = set()
        # check term exists in inverted index
        if term in self.inverted_index:
            # get relevant docs of term
            term_docs = self.inverted_index[term]['docs']
            # get docs id
            docs_id = set(term_docs.keys())

        return docs_id


    @staticmethod
    def create_postfix(query):
        precedence = {"NOT": 3, "AND": 2, "OR": 1}
        output = []
        stack = []

        for token in query:
            if token not in precedence and token not in {'(', ')'}:
                output.append(token)
            elif token in precedence:
                while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()  # Remove '('
                else:
                    raise ValueError("Mismatched parentheses")

        while stack:
            if stack[-1] in {'(', ')'}:
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())

        return output

    @staticmethod
    def evaluate_postfix(postfix_tokens, inverted_index, all_docs):
        stack = []

        for token in postfix_tokens:
            if token == 'AND':
                right = stack.pop()
                left = stack.pop()
                stack.append(left & right)
            elif token == 'OR':
                right = stack.pop()
                left = stack.pop()
                stack.append(left | right)
            elif token == 'NOT':
                operand = stack.pop()
                stack.append(all_docs - operand)
            else:
                # Lookup in inverted index
                stack.append(set(inverted_index.get(token.lower(), [])))

        return stack[0] if stack else set()