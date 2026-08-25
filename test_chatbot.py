
import unittest
from chatbot import ChatBot


class TestChatBot(unittest.TestCase):

    def setUp(self):
        self.bot = ChatBot(name="TestBot")

    def test_greeting_response(self):
        response = self.bot.get_response("hello")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_name_query(self):
        response = self.bot.get_response("what is your name?")
        self.assertIn("TestBot", response)

    def test_fallback_response(self):
        response = self.bot.get_response("asdkjhaskjdh random gibberish")
        self.assertIn(response, self.bot.fallback_responses)

    def test_history_is_recorded(self):
        self.bot.get_response("hi")
        history = self.bot.get_history()
        self.assertEqual(len(history), 2)  # user turn + bot turn
        self.assertEqual(history[0][0], "user")
        self.assertEqual(history[1][0], "bot")

    def test_time_query_returns_dynamic_content(self):
        response = self.bot.get_response("what time is it?")
        self.assertIn("current time", response.lower())


if __name__ == "__main__":
    unittest.main()
