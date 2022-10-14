from unittest import TestCase

from app import app, games
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
            response = client.post(
                '/api/new-game'
            )

            json_data = response.get_data(as_text=True)
            print(json.loads(json_data), "JSON LOADS")

            # returns true if json_data is JSON
            self.assertTrue(json.loads(json_data))

            # converting to python dictionary
            game_info = json.loads(json_data)

            # checking if the board game is in the global games dictionary
            self.assertTrue(game_info["gameId"] in games)
