from vison import BoardCV
from bot import WordHunter

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


def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip().lower() for line in file.readlines() if len(line.strip()) > 2]
    return words



def find_words(board, words):
    # Convert the board to lowercase
    board = [[char.lower() for char in row] for row in board]

    trie = Trie()
    for word in words:
        trie.insert(word)

    def dfs(node, i, j, path, current_word, coordinates):
        if node.is_end_of_word:
            result.add((current_word, tuple(coordinates)))  # Convert coordinates list to tuple
            node.is_end_of_word = False  # Mark as found to avoid duplicates

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            ni, nj = i + direction[0], j + direction[1]
            if 0 <= ni < 4 and 0 <= nj < 4 and (ni, nj) not in path:
                next_char = board[ni][nj]
                if next_char in node.children:
                    dfs(node.children[next_char], ni, nj, path | {(ni, nj)}, current_word + next_char, coordinates + [(ni, nj)])

    result = set()
    for i in range(4):
        for j in range(4):
            char = board[i][j]
            if char in trie.root.children:
                dfs(trie.root.children[char], i, j, {(i, j)}, char, [(i, j)])

    return sorted(list(result), key=lambda x: len(x[0]), reverse=True)

# Read words from a file
words_file_path = 'words.txt'
words = read_words_from_file(words_file_path)

def calculate_total_score(words):
    # Define the score mapping based on word length
    score_mapping = {
        3: 100,
        4: 400,
        5: 800,
        6: 1400,
        7: 1800,
        8: 2200,
        9: 2600,
        10: 3000,
        11: 3400,
        12: 3800
    }

    total_score = 0
    for word in words:
        word_length = len(word[0])
        if word_length in score_mapping:
            total_score += score_mapping[word_length]
    return total_score

boardCv = BoardCV()
boardCv.capture_board()
boardCv.process_board()
print(boardCv.get_board())

solutions = find_words(boardCv.get_board(), words)
score = calculate_total_score(solutions)
print(score)
wordHunter = WordHunter(solutions)
wordHunter.move_mouse_to_path()

   