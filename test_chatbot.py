"""
test_chatbot.py
----------------
Unit tests for the AI/ML Student Support ChatBot.

Run with:
    python -m unittest test_chatbot.py -v
"""

import unittest
from chatbot import ChatBot


class TestChatBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the model once for all tests (it's relatively expensive to load)
        cls.bot = ChatBot()

    def test_greeting_intent(self):
        result = self.bot.get_response_with_debug("hello there")
        self.assertEqual(result["predicted_intent"], "greeting")

    def test_library_hours_intent(self):
        result = self.bot.get_response_with_debug("what time does the library close")
        self.assertEqual(result["predicted_intent"], "library_hours")

    def test_tech_support_intent(self):
        result = self.bot.get_response_with_debug("i can't log into the portal")
        self.assertEqual(result["predicted_intent"], "tech_support")

    def test_response_is_nonempty_string(self):
        response = self.bot.get_response("when is the registration deadline")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_low_confidence_triggers_fallback(self):
        # Gibberish input should not confidently match any real intent
        result = self.bot.get_response_with_debug("asdkjh qweoiu zzxcv")
        self.assertLess(result["confidence"], 0.9)

    def test_history_is_recorded(self):
        bot = ChatBot()
        bot.get_response("hi")
        history = bot.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0][0], "user")
        self.assertEqual(history[1][0], "bot")


if __name__ == "__main__":
    unittest.main()
