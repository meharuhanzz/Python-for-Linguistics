# Day 2 — NLTK, Corpus Analysis with pandas, and Regex for Linguistic Patterns

## Schedule

1. Recap Day 1, Day 2 goals
2. Session 1 — NLTK: Tokenization, Frequency, Concordance
3. Session 2 — Corpus Analysis with pandas
4. Session 3 — Regular Expressions for Linguistic Patterns
5. Session 4 — Where Whitespace Tokenization Breaks (Indic preview)
6. Hands-on Lab — run and extend `exp1`, `exp2`, `exp3`
7. Wrap-up, Q&A, preview Day 3

## Learning objectives

By the end of Day 2, participants can:

- Use NLTK to tokenize, split sentences, compute frequency distributions, and run a
  concordance search on English text.
- Load a multilingual sentence corpus into a pandas DataFrame and compute per-language
  statistics: sentence count, vocabulary size, type-token ratio, average sentence
  length.
- Write and apply regex patterns to find linguistic patterns: prefixes, suffixes,
  repeated words, numbers, and simple part-of-speech-like surface cues.
- Explain, with a concrete example, why simple whitespace/punctuation tokenization is
  a reasonable default for English but an incomplete strategy for Malayalam, Hindi,
  and Tamil.

## Session 1 — NLTK

`word_tokenize`, `sent_tokenize`, `FreqDist`, and `nltk.Text.concordance` on the Day 1
English sample sentences. See `library_notes/01_nltk.md` for the concept background.

## Session 2 — Corpus Analysis with pandas

Load all four languages' sample sentences into one DataFrame with a `lang` column.
Compute vocabulary size and **type-token ratio** (unique words ÷ total words — a
standard corpus-linguistics measure of lexical diversity) per language, and discuss
why comparing raw counts across languages with very different average word lengths
(agglutinative Malayalam/Tamil vs. more analytic Hindi/English) needs care. See
`library_notes/02_pandas.md`.

## Session 3 — Regular Expressions for Linguistic Patterns

Building on `library_notes/00_python_stdlib_re_unicodedata.md`: prefix/suffix
patterns, finding numerals, finding repeated words, and a first (deliberately naive)
attempt at spotting a case marker by matching a suffix string. This naive attempt is
revisited critically in Day 4.

## Session 4 — Where Whitespace Tokenization Breaks (Indic preview)

A short, concrete look at what NLTK's/plain `.split()` tokenization does to a
morphologically dense Malayalam or Tamil sentence versus an English one of comparable
meaning — setting up Day 3's subword-tokenization comparison and Day 4's morphology
sessions, without yet introducing new tools.

## Experiments

| Script | Demonstrates | Languages |
|---|---|---|
| `exp1_nltk_tokenization_frequency.py` | NLTK tokenization, `FreqDist`, concordance | English (primary), contrasted with simple tokenization on ML/HI/TA |
| `exp2_pandas_corpus_analysis.py` | DataFrame corpus stats: vocab size, type-token ratio, sentence length | English, Malayalam, Hindi, Tamil |
| `exp3_regex_patterns.py` | Prefix/suffix search, numeral extraction, naive suffix-based case-marker search | English, Malayalam, Hindi, Tamil |

## Data

These experiments reuse `day1_python_basics_unicode/data/sentences_*.txt` rather than
duplicating the sample corpus — see that folder for the sentences and their notes.

## Going further

- Add a fifth sample sentence set (a language of your choice) and re-run
  `exp2_pandas_corpus_analysis.py` — which statistics still make sense to compare
  directly, and which need normalizing first (e.g. by word length)?
- In `exp3_regex_patterns.py`, try writing a suffix pattern that matches the Malayalam
  locative marker `ിൽ` and count how many "false positive" matches it produces on
  words where those letters aren't actually a case suffix.
