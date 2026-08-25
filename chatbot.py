
import random
import re
from datetime import datetime
from typing import List, Optional, Pattern, Tuple


class Rule:
    """A single pattern-response rule the bot can match against."""

    def __init__(self, pattern: str, responses: List[str]):
        self.pattern: Pattern = re.compile(pattern, re.IGNORECASE)
        self.responses: List[str] = responses

    def matches(self, text: str) -> bool:
        return self.pattern.search(text) is not None

    def get_response(self) -> str:
        return random.choice(self.responses)


class ChatBot:
    """A simple rule-based chatbot."""

    def __init__(self, name: str = "ChatBot"):
        self.name = name
        self.history: List[Tuple[str, str]] = []  # (speaker, message)
        self.rules: List[Rule] = self._build_rules()
        self.fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting — can you tell me more?",
            "I don't have an answer for that yet.",
            "Hmm, I didn't quite catch that. Try asking something else.",
        ]

    def _build_rules(self) -> List[Rule]:
        """Defines the bot's pattern -> response knowledge base.

        Add new Rule(...) entries here to extend what the bot understands.
        """
        return [
            Rule(r"\b(hi|hello|hey)\b", [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
            ]),
            Rule(r"\bhow are you\b", [
                "I'm just code, but I'm doing great! How about you?",
            ]),
            Rule(r"\byour name\b", [
                f"My name is {self.name}, a simple rule-based chatbot.",
            ]),
            Rule(r"\b(bye|goodbye|exit|quit)\b", [
                "Goodbye! Have a great day.",
            ]),
            Rule(r"\bhelp\b", [
                "I can respond to greetings, small talk, and basic "
                "questions about myself. Try asking 'how are you?' or "
                "'what time is it?'.",
            ]),
            Rule(r"\bthank(s| you)\b", [
                "You're welcome!",
            ]),
            Rule(r"\btime\b", [
                lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
            ]),
            Rule(r"\bdate\b", [
                lambda: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
            ]),
            Rule(r"\bjoke\b", [
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "I would tell you a UDP joke, but you might not get it.",
            ]),
        ]

    def _resolve_response(self, rule: Rule) -> str:
        """Rules may store plain strings or zero-arg callables (for dynamic
        content like the current time). This resolves either case."""
        response = rule.get_response()
        return response() if callable(response) else response

    def get_response(self, user_input: str) -> str:
        """Returns the bot's response to a single line of user input."""
        self.history.append(("user", user_input))

        for rule in self.rules:
            if rule.matches(user_input):
                response = self._resolve_response(rule)
                self.history.append(("bot", response))
                return response

        response = random.choice(self.fallback_responses)
        self.history.append(("bot", response))
        return response

    def get_history(self) -> List[Tuple[str, str]]:
        return self.history


def run_cli(bot: Optional[ChatBot] = None) -> None:
    """Runs an interactive command-line session with the chatbot."""
    bot = bot or ChatBot()
    print(f"{bot.name}: Hi! I'm {bot.name}. Type 'exit' or 'quit' to end our chat.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.name}: Goodbye!")
            break

        if not user_input:
            continue

        response = bot.get_response(user_input)
        print(f"{bot.name}: {response}")

        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input, re.IGNORECASE):
            break


if __name__ == "__main__":
    run_cli()
