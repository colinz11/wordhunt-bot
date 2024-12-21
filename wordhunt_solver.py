from vison import BoardCV
from bot import WordHunter
import pickle
import time
import cv2

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

    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)


def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip().lower() for line in file.readlines() if len(line.strip()) > 2]
    return words

def find_words(board, words):
    # Convert the board to lowercase
    board = [[char.lower() for char in row] for row in board]
    # Create a set of all characters on the board
    board_chars = {char for row in board for char in row}

    # Filter out words that cannot be formed using the characters on the board
    possible_words = [word for word in words if set(word).issubset(board_chars)]
    trie = Trie()
    for word in possible_words:
        trie.insert(word)


    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    result = set()

    def dfs_iterative(node, start_i, start_j):
        stack = [(node, start_i, start_j, {(start_i, start_j)}, board[start_i][start_j], [(start_i, start_j)])]
        while stack:
            node, i, j, path, current_word, coordinates = stack.pop()
            if node.is_end_of_word:
                result.add((current_word, tuple(coordinates)))  # Convert coordinates list to tuple
                node.is_end_of_word = False  # Mark as found to avoid duplicates

            for direction in directions:
                ni, nj = i + direction[0], j + direction[1]
                if 0 <= ni < 4 and 0 <= nj < 4 and (ni, nj) not in path:
                    next_char = board[ni][nj]
                    if next_char in node.children:
                        stack.append((node.children[next_char], ni, nj, path | {(ni, nj)}, current_word + next_char, coordinates + [(ni, nj)]))

    for i in range(4):
        for j in range(4):
            char = board[i][j]
            if char in trie.root.children:
                dfs_iterative(trie.root.children[char], i, j)
            
    
    return sorted(list(result), key=lambda x: len(x[0]), reverse=True)

# Read words from a file
words_file_path = 'wordbank.txt'
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
print(f'Max Score: {score}')
wordHunter = WordHunter(solutions)
wordHunter.move_mouse_to_path()

   