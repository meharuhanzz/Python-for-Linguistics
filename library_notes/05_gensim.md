# Gensim (Word2Vec)

```bash
pip install gensim
```

## Concept

Word2Vec answers a simple question: can you represent a word's *meaning* as a list of
numbers (a vector), such that words with similar meanings end up with similar vectors?
It does this by training on the idea that "you shall know a word by the company it
keeps" — words that tend to appear in similar surrounding contexts across a large
corpus get pushed toward similar vectors, purely from co-occurrence statistics, with
no dictionary or hand-built rules involved. This lets you compute things like "which
words are most similar to X" or the famous analogy arithmetic (king − man + woman ≈
queen) directly from vector math.

The key limitation to understand, not just accept: Word2Vec gives each word exactly
**one** vector, fixed regardless of context. A polysemous word (one with multiple
meanings, e.g. "bank" as riverbank vs. financial bank) gets one blended vector that
can't distinguish which sense is meant in a given sentence. Day 4 pairs this note with
`06_sentence_transformers.md`, which covers *contextual* embeddings — the modern fix
for exactly this limitation.

## Basic usage

```python
from gensim.models import Word2Vec

# a tiny toy corpus -- real training needs far more data than this;
# this is only enough to demonstrate the mechanics
sentences = [
    "the child read the book".split(),
    "the child read the story".split(),
    "the man read the newspaper".split(),
    "the woman read the book".split(),
]

model = Word2Vec(sentences, vector_size=20, window=3, min_count=1, epochs=100)

print(model.wv["book"])              # the vector itself (20 numbers)
print(model.wv.most_similar("book")) # words with the closest vectors
```

## Where this is used

Day 4's `exp3_word2vec_gensim.py` — training a small Word2Vec model on the tutorial's
own sample sentences (too small to be meaningful on its own — the point is watching
the mechanics work, not getting production-quality similarities) and inspecting its
word vectors, immediately followed by `exp4_contextual_vs_static_embeddings.py`, which
shows what a pretrained contextual model does differently on the same words.
