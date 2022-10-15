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
        # CREATING NEW GAME TO GET A NEW GAME ID
        game_info_json = new_game()
        # converting new game to python dictionary
        game_info = json.loads(game_info_json)

        with self.client as client:
            response = client.post(
                '/api/score-word', data={"word": "BAR", "gameId": game_info["gameId"]})
            json_response = response.get_json()  # THIS IS THE SERVER'S RESPONSE TO BROWSER
            game_id = game_info["gameId"]
            print(game_id, "<------ GAME IDDDDDD")
            games[game_id].board = [
                ["1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["B", "1", "1", "1", "1"],
                ["A", "1", "1", "1", "1"],
                ["R", "1", "1", "1", "1"]
            ]

            self.assertEqual({"result": "ok"}, json_response)
