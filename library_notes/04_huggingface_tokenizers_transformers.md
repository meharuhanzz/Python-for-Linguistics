# Hugging Face `tokenizers` / `transformers`

```bash
pip install transformers
```

`tokenizers` installs automatically as a dependency of `transformers` — no separate
install needed.

## Concept

Every modern language model needs to turn text into numbers before it can process it,
and *how* it splits text into pieces (tokens) before numbering them is itself a
linguistically meaningful choice. Older tools like NLTK/spaCy mostly split on
whitespace and punctuation, so a word is a token. Modern models instead use **subword
tokenization** (BPE, WordPiece, or SentencePiece are the three common algorithms):
they learn, from a large corpus, a vocabulary of frequent word-pieces, and split any
new word into pieces from that vocabulary — a rare or unseen word gets broken into
smaller, more frequent chunks rather than becoming a single "unknown word" token.

This matters directly for agglutinative languages like Malayalam and Tamil: a word
carrying several fused suffixes is genuinely rare as a *whole word*, even when its
stem and each suffix individually are common. Subword tokenization degrades much more
gracefully here than whitespace tokenization does — which is exactly why it's the
bridge into Day 4's discussion of morphology, and worth understanding as a concept
even before you use a full pretrained model.

`transformers` is the library that additionally gives you the pretrained models
themselves (e.g. multilingual or Indic-language BERT-style models) — used in this
tutorial's Day 4 for contextual embeddings, not for training anything from scratch.

## Basic usage

```python
from transformers import AutoTokenizer

# a multilingual tokenizer, so the same code works across languages
tok = AutoTokenizer.from_pretrained("google/muril-base-cased")

for word in ["book", "വീട്ടിലേക്ക്", "किताबों", "புத்தகத்தைப்"]:
    pieces = tok.tokenize(word)
    print(f"{word!r:20} -> {pieces}")
```

A short, common English word usually stays whole. A long, morphologically complex
Malayalam or Tamil word typically gets split into several pieces — stem-like pieces
plus suffix-like pieces — which is directly observable, not just a claim.

## Where this is used

Day 3's `exp3_subword_tokenization_comparison.py` — comparing token counts and splits
for the same kind of sentence across English/Malayalam/Hindi/Tamil. Day 4 reuses the
same tokenizer as part of loading a pretrained model for contextual embeddings.
