# Day 1 — Python Basics for Language Data & Unicode/Indic Script Handling

## Schedule

1. Welcome & Day 1 goals
2. Session 1 — Python Basics for Language Data
3. Session 2 — Unicode & Indic Script Handling
4. Session 3 — Reading & Structuring Corpora (file I/O)
5. Session 4 — Where Corpora Come From, Licensing & Ethics
6. Hands-on Lab — run and extend `exp1`, `exp2`
7. Wrap-up, Q&A, preview Day 2

## Learning objectives

By the end of Day 1, participants can:

- Use Python variables, strings, lists, dictionaries, loops, and functions to store
  and manipulate sentences, word lists, and annotated (e.g. POS-tagged) data.
- Explain the difference between bytes, Unicode code points, and grapheme clusters,
  and why this matters for Indic scripts specifically.
- Normalize Unicode text (NFC/NFD) and recognize common Indic encoding bugs (broken
  conjuncts, stray ZWJ/ZWNJ characters, mixed normalization forms in the same file).
- Read a small multilingual text corpus from disk into Python data structures.

## Session 1 — Python Basics for Language Data

Variables, strings, lists, dictionaries, loops, functions — taught entirely through
language examples rather than generic tutorials: a sentence is a string; a tokenized
sentence is a list of strings; a POS-tagged sentence is a list of `(word, tag)` tuples;
a small corpus is a list of sentences; word counts are a dictionary.

## Session 2 — Unicode & Indic Script Handling

Malayalam, Hindi, and Tamil text is not just "a string of characters" the way ASCII
English text is. A single visually-rendered character (like a conjunct consonant
cluster) can be composed of several Unicode code points, and the *same* visible text
can be encoded in more than one way (NFC vs. NFD normalization). This causes silent
bugs: two strings that look identical on screen can fail an `==` comparison, or a
`len()` call can report a surprising number.

Key ideas covered: code point vs. grapheme cluster, `unicodedata.normalize()`,
Zero-Width Joiner/Non-Joiner (ZWJ/ZWNJ) in Malayalam and Hindi conjuncts, and why you
should always normalize text to one form (typically NFC) immediately after reading it,
before doing anything else.

## Session 3 — Reading & Structuring Corpora

Reading `.txt` and `.csv` files with explicit `encoding="utf-8"`, splitting into
sentences/lines, and building a simple in-memory corpus structure (list of dicts:
`{"lang": ..., "text": ...}`) that later days' experiments reuse.

## Session 4 — Where Corpora Come From, Licensing & Ethics

A short, non-technical session: pointers to real corpora (Malayalam Wikipedia dumps,
AI4Bharat IndicCorp, institutional corpora), why licensing matters before
redistributing or publishing derived data, and a note on documenting provenance for
any corpus used in research.

## Library notes for today

- [`library_notes/00_python_stdlib_re_unicodedata.md`](../library_notes/00_python_stdlib_re_unicodedata.md)

## Experiments

| Script | Demonstrates | Languages |
|---|---|---|
| `exp1_basic_text_structures.py` | Storing sentences/word lists/POS-tagged data in Python structures; simple frequency counting with a plain dict | English, Malayalam, Hindi, Tamil |
| `exp2_unicode_normalization.py` | Code point vs. grapheme length, NFC vs. NFD, detecting normalization mismatches, ZWJ/ZWNJ inspection | English, Malayalam, Hindi, Tamil |

## Data

- `data/sentences_en.txt`, `data/sentences_ml.txt`, `data/sentences_hi.txt`,
  `data/sentences_ta.txt` — eight short hand-built sentences per language, reused
  throughout the whole 5-day tutorial. Several sentences deliberately vary only a
  case/tense/number marker (e.g. Malayalam `വീട്ടിൽ` "in the house" vs. `വീട്ടിലേക്ക്`
  "to the house") to set up Day 4's morphology discussion.

> These are small, simple teaching sentences, not a validated linguistic corpus. A
> native-speaker review is recommended before reusing them beyond this tutorial.

## Going further

- Try normalizing one of the sample files to NFD, saving it, then re-running
  `exp1_basic_text_structures.py` on both versions — do the word counts still match?
- Add a fifth language's sentence file following the same pattern and see which parts
  of `exp1`/`exp2` need no changes at all (most of it — that's the point).
