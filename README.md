# AI/ML Student Support ChatBot

An NLP-based chatbot that answers common student support questions
(office hours, registration deadlines, financial aid, library hours,
tech support, course selection, mental health resources, etc.) using a
trained **machine learning intent classification model** — not hardcoded
rules.

## How It Differs From a Rule-Based Bot

Instead of matching regular expressions, this bot:

1. Takes a labeled dataset of example student questions per intent
   (`data/intents.json`)
2. Converts text into numeric features using **TF-IDF vectorization**
   (unigrams + bigrams)
3. Trains a **Logistic Regression classifier** to predict the intent
   behind new, unseen input
4. At runtime, predicts the most likely intent for what the student typed
   and returns an appropriate response — including a confidence score
5. Falls back to "I'm not sure, let me connect you with a human advisor"
   when the model's confidence is too low, rather than guessing

This means the bot can generalize to phrasings it has never seen before,
as long as they're similar to the training examples — which is the core
idea behind NLP-based intent classification systems used in real chatbot
platforms (e.g., Dialogflow, Rasa).

## Project Structure

```
student_support_bot/
├── data/
│   └── intents.json          # Labeled training data (11 intents, ~200 examples)
├── model/
│   ├── intent_classifier.joblib   # Trained TF-IDF + LogisticRegression pipeline
│   └── intents_meta.json          # Response templates per intent
├── preprocessing.py           # Text cleaning (lowercase, punctuation removal)
├── train.py                   # Trains the model, prints evaluation metrics
├── chatbot.py                 # ChatBot class + CLI loop
├── main.py                    # Entry point
├── test_chatbot.py            # Unit tests
├── requirements.txt
└── README.md
```

## Intents Covered

`greeting`, `goodbye`, `thanks`, `office_hours`, `registration_deadline`,
`financial_aid`, `library_hours`, `tech_support`, `course_selection`,
`mental_health_support`, `escalate_human`

## Getting Started

### Requirements
- Python 3.8+
- scikit-learn, joblib (see `requirements.txt`)

### Installation
```bash
cd student_support_bot
pip install -r requirements.txt
```

### Training the Model
The trained model is already included, but you can retrain it (e.g.
after editing `data/intents.json`) with:
```bash
python train.py
```
This prints accuracy, a classification report, and a confusion matrix —
useful for your project report.

### Running the Chatbot
```bash
python main.py
```

Run with `--debug` to see the predicted intent and confidence score for
every message (useful for demos):
```bash
python main.py --debug
```

Example session:
```
Student Support Assistant: Hi! I'm here to help with student support questions.
You: when is the financial aid deadline
  [intent: financial_aid, confidence: 0.29]
Student Support Assistant: You can apply for financial aid through the FAFSA
at studentaid.gov. Your school's financial aid office can help with
scholarships and grants too.
```

### Running the Tests
```bash
python -m unittest test_chatbot.py -v
```

## Model Details

| Component | Choice | Why |
|---|---|---|
| Text vectorization | TF-IDF (unigrams + bigrams) | Captures word importance and short phrase context without needing a large corpus |
| Classifier | Logistic Regression | Fast to train, interpretable, performs well on small-to-medium labeled text datasets |
| Evaluation | Train/test split (80/20, stratified) | Standard supervised learning evaluation practice |
| Confidence threshold | 0.20 | Empirically chosen — with 11 classes, correct predictions typically score 0.20–0.50 rather than near 1.0, since probability mass spreads across all classes |

On the current dataset, the model achieves roughly **80%+ accuracy** on
held-out test examples (see console output from `train.py` for exact
figures, which vary slightly with data changes).

## Extending the Bot

To add a new intent:
1. Add a new entry to `data/intents.json` with a `tag`, a list of
   example phrases (10+ recommended), and a list of `responses`.
2. Re-run `python train.py` to retrain the model.

## Limitations & Future Work

- Training data is hand-written and relatively small — a production
  system would use real historical student queries for training.
- No conversation context/memory across turns (each message is
  classified independently).
- Could be extended with:
  - A larger, more diverse labeled dataset
  - Named Entity Recognition (e.g., extracting course codes, dates)
  - A deep learning model (e.g., fine-tuned BERT) for higher accuracy
  - Integration with a real LLM for open-domain fallback questions
  - A web front-end and persistent conversation logging

## Author

Submitted as a college AI/ML project. Built with Python, scikit-learn
(TF-IDF + Logistic Regression), and standard NLP preprocessing.
