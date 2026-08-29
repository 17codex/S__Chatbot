"""
main.py
-------
Entry point for the AI/ML Student Support ChatBot.

Usage:
    python main.py            # normal chat
    python main.py --debug    # also shows predicted intent + confidence
"""

import sys
from chatbot import ChatBot, run_cli


def main():
    debug = "--debug" in sys.argv
    bot = ChatBot()
    run_cli(bot, debug=debug)


if __name__ == "__main__":
    main()
