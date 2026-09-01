"""
Day 1, Experiment 1: Basic Python structures for language data.

Concepts: variables, strings, lists, dictionaries, loops, functions.
Languages: English, Malayalam, Hindi, Tamil.

Run: python3 exp1_basic_text_structures.py
"""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

LANGUAGES = {
    "en": "English",
    "ml": "Malayalam",
    "hi": "Hindi",
    "ta": "Tamil",
}


# ---------------------------------------------------------------------------
# Step 1: a sentence is just a string.
# ---------------------------------------------------------------------------
sample_sentence = "The child read the book again."
print("A sentence is a string:")
print(" ", repr(sample_sentence))
print(" length in characters:", len(sample_sentence))
print()


# ---------------------------------------------------------------------------
# Step 2: load each language's corpus into a list of strings (one per line).
# ---------------------------------------------------------------------------
def load_sentences(lang_code: str) -> list[str]:
    """Read data/sentences_<lang_code>.txt into a list of sentence strings."""
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


corpora: dict[str, list[str]] = {}
for code in LANGUAGES:
    corpora[code] = load_sentences(code)

print("A corpus is a list of sentence strings:")
for code, name in LANGUAGES.items():
    print(f"  {name}: {len(corpora[code])} sentences")
    print(f"    first sentence -> {corpora[code][0]!r}")
print()


# ---------------------------------------------------------------------------
# Step 3: a tokenized sentence is a list of word strings.
# We use the simplest possible tokenizer here (whitespace + strip punctuation)
# on purpose — Day 2 introduces NLTK's real tokenizers, and Day 3 shows where
# whitespace tokenization breaks down for Indic scripts.
# ---------------------------------------------------------------------------
PUNCT = ".,!?;:।"  # includes the Devanagari/Indic danda "।" used as a full stop


def simple_tokenize(sentence: str) -> list[str]:
    """Split on whitespace, then strip common punctuation from each token."""
    tokens = []
    for word in sentence.split():
        cleaned = word.strip(PUNCT)
        if cleaned:
            tokens.append(cleaned)
    return tokens


print("A tokenized sentence is a list of word strings:")
for code, name in LANGUAGES.items():
    tokens = simple_tokenize(corpora[code][0])
    print(f"  {name}: {tokens}")
print()


# ---------------------------------------------------------------------------
# Step 4: word frequency is a dictionary mapping word -> count.
# ---------------------------------------------------------------------------
def word_frequencies(sentences: list[str]) -> dict[str, int]:
    """Count how many times each word (after simple tokenization) appears."""
    freq: dict[str, int] = {}
    for sentence in sentences:
        for token in simple_tokenize(sentence):
            freq[token] = freq.get(token, 0) + 1
    return freq


print("Word frequencies (top 3 most common word per language):")
for code, name in LANGUAGES.items():
    freq = word_frequencies(corpora[code])
    top3 = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:3]
    print(f"  {name}: {top3}")
print()


# ---------------------------------------------------------------------------
# Step 5: a POS-tagged sentence is a list of (word, tag) tuples.
# We hand-tag one English example here; Day 3 (spaCy) automates this.
# ---------------------------------------------------------------------------
hand_tagged_example = [
    ("The", "DET"),
    ("child", "NOUN"),
    ("read", "VERB"),
    ("the", "DET"),
    ("book", "NOUN"),
    ("again", "ADV"),
]
print("A POS-tagged sentence is a list of (word, tag) tuples:")
print(" ", hand_tagged_example)


if __name__ == "__main__":
    pass
