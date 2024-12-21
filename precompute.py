import pickle

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)


def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip().lower() for line in file.readlines() if len(line.strip()) > 2]
    return words

# Precompute the trie
words_file_path = 'wordbank.txt'
words = read_words_from_file(words_file_path)
trie = Trie()
for word in words:
    trie.insert(word)

# Save the trie to a file
trie.save('trie.pkl')