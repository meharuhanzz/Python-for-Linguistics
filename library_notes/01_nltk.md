# NLTK (Natural Language Toolkit)

```bash
pip install nltk
python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

## Concept

NLTK is the oldest and most teaching-oriented Python NLP library — it was built for
exactly the audience of this tutorial: people learning what computational text
analysis *is*, not just how to call an API. It provides the classic building blocks of
corpus linguistics as simple functions: split text into sentences, split sentences
into words (tokenization), count word frequencies, find a word in its surrounding
context (a concordance, the computational version of a KWIC — Key Word In Context —
index used in traditional corpus linguistics), and filter out very common function
words (stopwords).

NLTK's tokenizers and taggers are trained mainly on English and a handful of other
languages — they don't have built-in support for Malayalam, Hindi, or Tamil. That's
not a flaw to work around quietly; it's a genuine, useful fact about the current state
of NLP tooling, and Day 2's experiments show both what NLTK gets right on English and
where you have to fall back to simpler whitespace/regex-based approaches for Indic text.

## Basic usage

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist

text = "The child read the book. The child liked the book a lot."

sentences = sent_tokenize(text)
print(sentences)
# ['The child read the book.', 'The child liked the book a lot.']

words = word_tokenize(text.lower())
freq = FreqDist(words)
print(freq.most_common(3))
# [('the', 4), ('.', 2), ('child', 2)]

# concordance: find a word in its surrounding context
text_obj = nltk.Text(words)
text_obj.concordance("book")
```

## Where this is used

Day 2's `exp1_nltk_tokenization_frequency.py` — tokenization, frequency distribution,
and concordance search, run on the English sample data and contrasted against a
simple regex tokenizer applied to the Malayalam/Hindi/Tamil sample data.
