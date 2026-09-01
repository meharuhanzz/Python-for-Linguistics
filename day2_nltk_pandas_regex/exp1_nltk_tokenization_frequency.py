"""
Day 2, Experiment 1: NLTK tokenization, frequency distribution, and concordance.

Concepts: sentence/word tokenization, FreqDist, concordance (KWIC) search.
Languages: English (NLTK's tokenizers are trained for this), contrasted with a
simple whitespace tokenizer applied to Malayalam/Hindi/Tamil to show the gap.

See library_notes/01_nltk.md for background before/while working through this.

Setup (only needed once):
    python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

Run: python3 exp1_nltk_tokenization_frequency.py
"""

from pathlib import Path

import nltk
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


en_sentences = load_sentences("en")
en_text = " ".join(en_sentences)


# ---------------------------------------------------------------------------
# Step 1: sentence tokenization.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Sentence tokenization (English, via NLTK)")
print("=" * 60)
split_sentences = sent_tokenize(en_text)
print(f"Original had {len(en_sentences)} lines; NLTK found {len(split_sentences)} sentences.")
for s in split_sentences[:3]:
    print(" ", s)
print()


# ---------------------------------------------------------------------------
# Step 2: word tokenization -- NLTK is smarter than plain .split() because it
# separates punctuation from words correctly ("house." -> "house", ".").
# ---------------------------------------------------------------------------
print("=" * 60)
print("Word tokenization: NLTK vs. plain .split()")
print("=" * 60)
example = en_sentences[0]
print(f"Sentence: {example!r}")
print(f"  plain .split()   -> {example.split()}")
print(f"  nltk word_tokenize -> {word_tokenize(example)}")
print("Notice NLTK correctly separates the trailing period from 'house'.")
print()


# ---------------------------------------------------------------------------
# Step 3: frequency distribution over the whole English sample corpus.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Frequency distribution (English)")
print("=" * 60)
all_tokens = [tok.lower() for tok in word_tokenize(en_text) if tok.isalpha()]
freq = FreqDist(all_tokens)
print("Most common 5 words:", freq.most_common(5))
print()


# ---------------------------------------------------------------------------
# Step 4: concordance -- see a word in its surrounding context, the
# computational version of a KWIC (Key Word In Context) index.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Concordance for 'book'")
print("=" * 60)
nltk_text = nltk.Text(word_tokenize(en_text))
nltk_text.concordance("book", width=60)
print()


# ---------------------------------------------------------------------------
# Step 5: the Indic contrast. NLTK's word_tokenize is not designed for
# Malayalam/Hindi/Tamil; here we fall back to the simple regex-based
# tokenizer from Day 1 and compare token counts to plain whitespace split,
# to make the "what does a real tokenizer buy you" question concrete rather
# than abstract.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Indic contrast: NLTK's English tokenizer is not a universal tool")
print("=" * 60)
for lang in ("ml", "hi", "ta"):
    sentences = load_sentences(lang)
    example = sentences[0]
    whitespace_tokens = example.split()
    nltk_attempt = word_tokenize(example)  # NLTK will still run, just not tuned for this script
    print(f"{lang}: {example!r}")
    print(f"  whitespace split : {whitespace_tokens}")
    print(f"  nltk word_tokenize (English-trained, applied anyway): {nltk_attempt}")
print()
print("Look closely: NLTK still splits off the ASCII period '.' for Malayalam and")
print("Tamil -- but that's not Malayalam/Tamil-specific knowledge, it's the same")
print("generic ASCII-punctuation rule it would apply to any text. For Hindi, the")
print("sentence ends with the Devanagari danda '।' instead of '.', which NLTK's")
print("English-trained rules don't recognize as sentence-final punctuation at all --")
print("so it stays glued to the last word. In no case is NLTK using real")
print("Malayalam/Hindi/Tamil linguistic knowledge here. Day 3 shows a tool (subword")
print("tokenization) that behaves meaningfully differently across all four languages.")


if __name__ == "__main__":
    pass
