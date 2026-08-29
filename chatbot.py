"""
chatbot.py
----------
Core logic for the AI/ML-based Student Support ChatBot.

Unlike a purely rule-based bot, this version uses a trained NLP pipeline
(TF-IDF vectorization + Logistic Regression classifier) to predict the
*intent* behind a student's message, then returns an appropriate response
for that intent.

If the model's confidence in its top prediction is below a threshold, the
bot treats the input as unrecognized and offers to escalate to a human
advisor rather than guessing.
"""

import json
import random
from typing import List, Tuple

import joblib

from preprocessing import clean_text

MODEL_PATH = "model/intent_classifier.joblib"
INTENTS_META_PATH = "model/intents_meta.json"
CONFIDENCE_THRESHOLD = 0.20  # below this, the bot admits it doesn't know
# Note: with 11 intent classes, a "confident" top prediction often sits in the
# 0.20-0.40 range rather than near 1.0, since probability mass is spread
# across all classes. The threshold is tuned empirically against the
# validation examples in train.py rather than fixed at a high value.


class ChatBot:
    """AI/ML-based Student Support ChatBot using NLP intent classification."""

    def __init__(self, name: str = "Student Support Assistant"):
        self.name = name
        self.history: List[Tuple[str, str]] = []
        self.model = joblib.load(MODEL_PATH)
        with open(INTENTS_META_PATH, "r") as f:
            self.responses_by_tag = json.load(f)

        self.fallback_responses = [
            "I'm not confident I understood that. Could you rephrase, or "
            "would you like me to connect you with a human advisor?",
            "I don't have a good answer for that yet. Try rephrasing, or "
            "I can flag it for a staff member to follow up.",
        ]

    def predict_intent(self, text: str) -> Tuple[str, float]:
        """Returns (predicted_tag, confidence) for a piece of input text."""
        cleaned = clean_text(text)
        probs = self.model.predict_proba([cleaned])[0]
        classes = self.model.classes_
        best_idx = probs.argmax()
        return classes[best_idx], float(probs[best_idx])

    def get_response(self, user_input: str) -> str:
        """Returns the bot's response to a single line of user input."""
        self.history.append(("user", user_input))

        tag, confidence = self.predict_intent(user_input)

        if confidence >= CONFIDENCE_THRESHOLD and tag in self.responses_by_tag:
            response = random.choice(self.responses_by_tag[tag])
        else:
            response = random.choice(self.fallback_responses)
            tag = "fallback"

        self.history.append(("bot", response))
        return response

    def get_response_with_debug(self, user_input: str) -> dict:
        """Like get_response, but also returns the predicted intent and
        confidence score — useful for the report / demo / debugging."""
        tag, confidence = self.predict_intent(user_input)
        response = self.get_response(user_input)
        return {
            "input": user_input,
            "predicted_intent": tag,
            "confidence": round(confidence, 3),
            "response": response,
        }

    def get_history(self) -> List[Tuple[str, str]]:
        return self.history


def run_cli(bot: "ChatBot" = None, debug: bool = False) -> None:
    """Runs an interactive command-line session with the chatbot."""
    bot = bot or ChatBot()
    print(f"{bot.name}: Hi! I'm here to help with student support questions. "
          f"Type 'exit' or 'quit' to end.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.name}: Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print(f"{bot.name}: Goodbye! Good luck with your studies.")
            break

        if debug:
            result = bot.get_response_with_debug(user_input)
            print(f"  [intent: {result['predicted_intent']}, "
                  f"confidence: {result['confidence']}]")
            print(f"{bot.name}: {result['response']}")
        else:
            response = bot.get_response(user_input)
            print(f"{bot.name}: {response}")


if __name__ == "__main__":
    run_cli(debug=True)
