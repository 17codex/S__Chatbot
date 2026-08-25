# ChatBot — Rule-Based Conversational Agent

A simple rule-based chatbot implemented in Python. The bot uses regular
expression pattern matching to recognize user intents and respond with
appropriate, sometimes dynamically generated, replies.

## Features

- Pattern-based intent matching using regular expressions
- Multiple candidate responses per intent (chosen at random for variety)
- Dynamic responses (e.g., current time/date)
- Conversation history tracking
- Fallback handling for unrecognized input
- Command-line interface for interactive chatting
- Unit test suite

## Project Structure

```
chatbot_project/
├── main.py            # Entry point — run this to start chatting
├── chatbot.py          # Core ChatBot class and rule engine
├── test_chatbot.py     # Unit tests
├── requirements.txt    # Dependencies (none beyond the standard library)
└── README.md           # This file
```

## How It Works

The `ChatBot` class holds a list of `Rule` objects. Each rule pairs a
regular expression pattern with one or more possible responses. When the
user sends a message:

1. The bot checks the message against each rule's pattern, in order.
2. On the first match, it returns one of that rule's responses
   (selected at random, or computed dynamically for things like time/date).
3. If no rule matches, a random fallback response is returned.

All exchanges are stored in `self.history` as `(speaker, message)` tuples,
which could be used later for logging, analytics, or export.

## Getting Started

### Requirements
- Python 3.8+

### Installation
No external dependencies are required — the project only uses the Python
standard library.

```bash
git clone <your-repo-url>
cd chatbot_project
```

### Running the Chatbot
```bash
python main.py
```

Example session:
```
ChatBot: Hi! I'm ChatBot. Type 'exit' or 'quit' to end our chat.
You: hello
ChatBot: Hi there! What's on your mind?
You: what time is it?
ChatBot: The current time is 14:32:10.
You: bye
ChatBot: Goodbye! Have a great day.
```

### Running the Tests
```bash
python -m unittest test_chatbot.py -v
```

## Extending the Bot

New conversational capabilities can be added by inserting new `Rule`
entries in `ChatBot._build_rules()` in `chatbot.py`:

```python
Rule(r"\bweather\b", ["I can't check live weather yet, but it looks nice today!"])
```

## Possible Future Improvements

- Replace regex matching with an NLP intent classifier (e.g., using
  scikit-learn or spaCy)
- Add persistent conversation logging to a file or database
- Connect to a large language model API for open-domain responses
- Build a web or GUI front-end instead of the CLI

## Author

Submitted as a college project. Built with Python's standard library
(`re`, `random`, `datetime`) — no external dependencies required.
