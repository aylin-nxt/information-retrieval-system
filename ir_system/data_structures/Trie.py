class TrieNode:
    def __init__(self):
        self.children = {}       # key: character, value: TrieNode
        self.is_end_of_word = False

class Trie:
    def __init__(self, docs):
        self.root = TrieNode()
        self.docs = docs
        self.insert_tokens()

    def insert_tokens(self):
        tokens_set = self.creating_tokens_set()
        # loop over every token
        for token in tokens_set:
            # add $ to end of token
            tokens_rotation = token + "$"
            # rotate $ in term for each term
            for i in range(len(tokens_rotation)):
                # rotate $
                term = tokens_rotation[i:] + tokens_rotation[:i]
                # insert into trie
                self.insert(term)

    def creating_tokens_set(self):
        # initialize token set
        tokens_set = set()
        # add each token of documents to one set
        for docId, tokens in self.docs.items():
            tokens_set.update(tokens)
        # return final result( set of tokens )
        return tokens_set

    def insert(self, word: str):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> list:
        def dfs(node, prefix, results):
            if node.is_end_of_word:
                results.append(prefix)
            for char, child in node.children.items():
                dfs(child, prefix + char, results)

        results = []
        current = self.root
        for char in prefix:
            if char not in current.children:
                return results
            current = current.children[char]
        dfs(current, prefix, results)
        return results
