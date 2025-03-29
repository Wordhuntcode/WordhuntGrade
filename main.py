# main.py

def load_words(filename):
    """Load words from a text file into a set."""
    with open(filename, 'r') as file:
        valid_words = set(word.strip().lower() for word in file if len(word.strip()) >= 3)
    return valid_words

def get_prefixes(words):
    """Get all prefixes from the word list for early pruning."""
    prefixes = set()
    for word in words:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])
    return prefixes

def input_board():
    """Get the 4x4 Word Hunt board from user input."""
    print("Enter the 4x4 Word Hunt board, one row at a time (4 letters per row):")
    board = []
    for i in range(4):
        row = input(f"Row {i + 1}: ").strip().lower()
        if len(row) != 4 or not row.isalpha():
            print("Each row must be 4 letters. Try again.")
            return input_board()
        board.append(list(row))
    return board

def print_board(board):
    print("\nBoard:")
    for row in board:
        print(" ".join(row))

def get_neighbors(x, y, size=4):
    """Return all valid neighboring cells in 8 directions."""
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))
    return neighbors

def dfs(board, x, y, visited, current_word, dictionary, prefixes, found_words):
    """Recursive DFS to build words from the board."""
    current_word += board[x][y]
    visited.add((x, y))

    if current_word not in prefixes:
        visited.remove((x, y))
        return

    if current_word in dictionary:
        found_words.add(current_word)

    for nx, ny in get_neighbors(x, y):
        if (nx, ny) not in visited:
            dfs(board, nx, ny, visited, current_word, dictionary, prefixes, found_words)

    visited.remove((x, y))

def find_all_words(board, dictionary, prefixes):
    found_words = set()
    for x in range(4):
        for y in range(4):
            dfs(board, x, y, set(), '', dictionary, prefixes, found_words)
    return found_words

def score_word(word):
    """Score words using GamePigeon Word Hunt rules."""
    length = len(word)
    if length == 3:
        return 100
    elif length == 4:
        return 400
    elif length == 5:
        return 800
    elif length == 6:
        return 1400
    elif length == 7:
        return 1800
    elif length == 8:
        return 2200
    elif length == 9:
        return 2600
    elif length == 10:
        return 3000
    elif length == 11:
        return 3400
    elif length == 12:
        return 3800
    elif length == 13:
        return 4200
    elif length > 13:
        return 4200 + (length - 13) * 400  # Optional: keep scaling
    else:
        return 0

def main():
    dictionary = load_words("words.txt")
    print(f"{len(dictionary)} words loaded into dictionary.")
    print("Example words:", list(dictionary)[:10])
    prefixes = get_prefixes(dictionary)
    board = input_board()
    print_board(board)

    print("\nSearching for words...")
    valid_words = find_all_words(board, dictionary, prefixes)
    scored_words = [(word, score_word(word)) for word in valid_words]
    scored_words.sort(key=lambda x: (-x[1], x[0]))  # sort by score desc, then alphabetically

    max_score = sum(score for _, score in scored_words)

    print(f"\n🔍 Found {len(valid_words)} valid words. Max possible score: {max_score}\n")
    for word, score in scored_words:
        print(f"{word} ({score})")

    your_score = input("\nEnter your actual Word Hunt score: ")
    try:
        your_score = int(your_score)
        percentage = (your_score / max_score) * 100 if max_score > 0 else 0
        print(f"\n✅ Your Score: {your_score}")
        print(f"🎯 Max Possible Score: {max_score}")
        print(f"📊 You scored {percentage:.2f}% of the possible points.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

if __name__ == "__main__":
    main()
