from flask import Flask, request, jsonify
from flask_cors import CORS
from main import load_words, get_prefixes, find_all_words, score_word

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from the HTML page

dictionary = load_words("words.txt")
prefixes = get_prefixes(dictionary)

@app.route("/api/score", methods=["POST"])
def score_grid():
    data = request.get_json()
    board = data.get("board")

    if not board or len(board) != 4 or any(len(row) != 4 for row in board):
        return jsonify({"error": "Invalid board format"}), 400

    found_words = find_all_words(board, dictionary, prefixes)
    scored_words = [(w, score_word(w)) for w in found_words]
    scored_words.sort(key=lambda x: (-x[1], x[0]))
    total_score = sum(score for _, score in scored_words)

    return jsonify({
        "max_score": total_score,
        "word_count": len(found_words),
        "words": scored_words
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
