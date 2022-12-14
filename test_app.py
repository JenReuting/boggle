from unittest import TestCase

from app import app, games, new_game
import json


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="word-input-btn">Go</button>', html)
            self.assertIn('Go</button>', html)
            self.assertIn('home page template', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')

            # json_data = python dictionary
            json_data = response.get_json()

            # checking if the board game is in the global games dictionary
            self.assertTrue(json_data["gameId"] in games)

            # check if typeof game_id == string
            self.assertTrue(type(json_data["gameId"]) == str)

            # check if board is comprised of list of lists
            self.assertTrue(any(isinstance(
                sub_list, list) for sub_list in json_data["board"]))

    def test_score_word(self):
        """Testing word validation when a new word is submitted"""
        with self.client as client:
            response = client.post('/api/new-game')

        game_info = response.get_json()
        # creating game_id variable and assigning it to the current game id
        game_id = game_info["gameId"]
        # creating a mock game board
        games[game_id].board = [
            ["1", "1", "1", "1", "1"],
            ["1", "1", "1", "1", "1"],
            ["B", "1", "1", "1", "1"],
            ["A", "1", "1", "1", "1"],
            ["R", "1", "1", "1", "1"]
        ]

        with self.client as client:
            response = client.post(
                '/api/score-word', json={"word": "BAR", "gameId": game_id})
            json_response = response.get_json()

            self.assertEqual({"result": "ok"}, json_response)

        with self.client as client:
            response = client.post(
                '/api/score-word', json={"word": "ASDLFK", "gameId": game_id})
            json_response = response.get_json()

            self.assertEqual({"result": "not word"}, json_response)

        with self.client as client:
            response = client.post(
                '/api/score-word', json={"word": "CAT", "gameId": game_id})
            json_response = response.get_json()

            self.assertEqual({"result": "not-on-board"}, json_response)
