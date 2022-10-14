from flask import Flask, request, render_template, jsonify
from uuid import uuid4
from boggle import BoggleGame


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""
    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    game_info = {"gameId": game_id, "board": game.board}

    return jsonify(game_info)

@app.post("/api/score-word")
def score_word():

    request_data = request.json
    word = request_data["word"]
    game_id = request_data["gameId"]

    current_game = games[game_id]

    if not current_game.is_word_in_word_list(word):
        response = {"result": "not word"}

    elif not current_game.check_word_on_board(word):
        response = {"result": "not-on-board"}

    else:
        response = {"result": "ok"}

    return jsonify(response)