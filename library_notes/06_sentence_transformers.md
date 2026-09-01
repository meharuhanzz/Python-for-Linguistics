# `sentence-transformers` (contextual embeddings)

```bash
pip install sentence-transformers
```

## Concept

`sentence-transformers` wraps pretrained transformer models (like BERT-family models)
to produce **contextual** embeddings: a vector for a word or sentence that depends on
the *surrounding context*, not just the word itself. This is the direct answer to
Word2Vec's one-vector-per-word limitation (see `05_gensim.md`): the same word gets a
different vector in different sentences, so a model can (in principle) tell apart
"bank" the riverbank from "bank" the financial institution, or in Malayalam, correctly
distinguish two sentences that differ only in a single morphological suffix — the exact
kind of case/tense/negation distinction this tutorial keeps coming back to.

Practically, it also gives you sentence-level (not just word-level) vectors directly,
and a one-line cosine-similarity function — useful for tasks like "which of these
sentences means roughly the same thing" or "find the most similar sentence in a
corpus to this query", which come up constantly in corpus and translation work.

## Basic usage

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

sentences = [
    "The child went to the house.",
    "The child went towards the house.",
    "The train was late.",
]

embeddings = model.encode(sentences)
similarity = util.cos_sim(embeddings[0], embeddings[1])
print(similarity)  # high: similar meaning
similarity2 = util.cos_sim(embeddings[0], embeddings[2])
print(similarity2)  # low: unrelated meaning
```

To see the *contextual* part specifically (the same word getting different vectors),
encode the same word embedded in two different sentences and compare those sub-vectors
— `exp4_contextual_vs_static_embeddings.py` does this explicitly against Word2Vec's
single fixed vector for the same word.

## Where this is used

Day 4's `exp4_contextual_vs_static_embeddings.py` — same-word-different-sentence
comparison across English, Malayalam, Hindi, and Tamil examples, directly following
the Word2Vec experiment so the contrast is visible back to back.
