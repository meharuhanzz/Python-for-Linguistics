# Day 4 — Morphology: Regex vs. FST, and Embeddings: Static vs. Contextual

## Schedule

| Time | Block |
|---|---|
| 10:00–10:15 | Recap Day 3, Day 4 goals |
| 10:15–11:15 | **Session 1** — Regex-Based Morphology and Where It Breaks |
| 11:15–11:25 | Tea Break |
| 11:25–12:30 | **Session 2** — FST-Based Morphological Analysis (`mlmorph`, Malayalam) |
| 12:30–1:30 | Lunch Break |
| 1:30–2:30 | **Session 3** — Word2Vec: Static Word Embeddings |
| 2:30–2:40 | Tea Break |
| 2:40–3:40 | **Session 4** — Contextual Embeddings and Why They Differ |
| 3:40–4:40 | **Hands-on Lab** — run and extend `exp1`–`exp4` |
| 4:40–5:00 | Wrap-up, Q&A, preview Day 5 |

## Learning objectives

By the end of Day 4, participants can:

- Give a concrete example of a regex suffix-matching rule producing a false-positive
  match, and explain *why* regex cannot distinguish that case from a true match.
- Explain what a finite-state transducer (FST) morphological analyzer does
  differently from regex, and what "round-trip validation" (analyse → mutate →
  generate → re-analyse) buys you.
- Train a small Word2Vec model and retrieve nearest-neighbour words from it.
- Explain, with a worked example, why a static embedding (Word2Vec) cannot
  distinguish two senses/contexts of the same word, and show a contextual embedding
  (transformer-based) doing so.

## Session 1 — Regex-Based Morphology and Where It Breaks

Direct continuation of Day 2 Session 3/4's naive suffix search. Here we deliberately
construct false-positive cases: words that end in a case-marker-shaped string but
where that ending is part of the stem, not a suffix. The lesson is structural, not
about writing a "better" regex — no regex, however cleverly written, can encode "is
this actually a valid stem+suffix combination in the language" without effectively
reimplementing a morphological model by hand.

## Session 2 — FST-Based Morphological Analysis

Introduces `mlmorph` as the correct tool for the Session 1 problem: **analysis**
(surface word → stem + grammatical tags) and **generation** (stem + tags → surface
word), with round-trip validation as the way to check any mutation you generate is
actually well-formed. See `library_notes/07_mlmorph_fst_morphology.md` for install
notes — this session's experiment degrades gracefully if `mlmorph` isn't installed.

## Session 3 — Word2Vec: Static Word Embeddings

Train a small model on the tutorial's own sentences, inspect the resulting vectors,
and retrieve nearest neighbours. See `library_notes/05_gensim.md`.

## Session 4 — Contextual Embeddings and Why They Differ

The direct fix to Word2Vec's one-vector-per-word limitation: encode the *same* word
inside two different sentences with a pretrained transformer model and observe that
the vectors differ, unlike Word2Vec's fixed lookup. See
`library_notes/06_sentence_transformers.md`.

## Experiments

| Script | Demonstrates | Languages |
|---|---|---|
| `exp1_regex_morphology_limits.py` | Constructed false-positive suffix matches | Malayalam (primary), Tamil |
| `exp2_fst_morphology_malayalam.py` | Correct analysis/generation with round-trip validation, with a graceful fallback if `mlmorph` isn't installed | Malayalam |
| `exp3_word2vec_gensim.py` | Training a toy Word2Vec model, nearest-neighbour retrieval | English, Malayalam, Hindi, Tamil (separate toy corpora) |
| `exp4_contextual_vs_static_embeddings.py` | Same word, two contexts, two different contextual vectors vs. one fixed Word2Vec vector | English, Malayalam, Hindi, Tamil |

## Data

Reuses `day1_python_basics_unicode/data/sentences_*.txt` where relevant; `exp3`
builds slightly larger toy sentence sets inline (Word2Vec needs more repetition than
the 8-sentence sample corpus provides to produce any meaningful neighbours at all).

## Going further

- In `exp1`, try to write a regex complex enough to rule out your own false-positive
  example. Can you do it without hand-encoding a list of known stems — i.e. without
  secretly building a small lexicon inside the regex?
- In `exp4`, find a genuinely polysemous word in one of the four languages (a word
  with two unrelated meanings, not just two grammatical forms) and test whether the
  contextual model actually separates its two senses.
