# Python for Linguistics — 5-Day Tutorial

**Author / Maintainer:** [meharuhanzz](https://github.com/meharuhanzz) (sole
contributor and maintainer of this repo)

A hands-on, beginner-friendly tutorial for using Python in corpus linguistics,
morphology, syntax, semantics, annotation, and NLP — with worked examples in
**English, Malayalam, Hindi, and Tamil**.

This repo is designed to grow: each day is a self-contained folder with a `DAYx.md`
guide and numbered experiment scripts. Adding a new experiment is as simple as
dropping a new `expN_*.py` file into the relevant day's folder and linking it from
that day's `DAYx.md` — see [Extending this tutorial](#extending-this-tutorial).

## Who this is for

Linguistics students and researchers with little or no programming background who
want to apply Python to real language data: corpus building, annotation, morphological
analysis, syntactic parsing, and semantic similarity — across a mix of a
well-resourced language (English) and three Indian languages at different points on
the morphological-complexity spectrum (Malayalam and Tamil are highly agglutinative,
Hindi much less so).

## Structure

| Day | Folder | Focus |
|---|---|---|
| 1 | [`day1_python_basics_unicode/`](day1_python_basics_unicode/DAY1.md) | Python fundamentals for language data, Unicode & Indic script handling |
| 2 | [`day2_nltk_pandas_regex/`](day2_nltk_pandas_regex/DAY2.md) | NLTK, corpus analysis with pandas, regex for linguistic patterns |
| 3 | [`day3_spacy_subword_tokenization/`](day3_spacy_subword_tokenization/DAY3.md) | spaCy annotation pipelines, subword tokenization (BPE/WordPiece/SentencePiece) |
| 4 | [`day4_morphology_embeddings/`](day4_morphology_embeddings/DAY4.md) | Regex vs. FST-based morphology, static vs. contextual word embeddings |
| 5 | [`day5_capstone_project/`](day5_capstone_project/DAY5.md) | Mini linguistic data project combining all four days, research applications |

Every library used across the five days also has its own short concept-plus-usage note
in [`library_notes/`](library_notes/README.md) — read the relevant note before (or
alongside) the day that introduces it, separately from the experiment script itself.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 -m spacy download en_core_web_sm
python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng')"
```

Malayalam-specific FST morphology (Day 4, optional deep-dive) needs `mlmorph`
separately — see [`day4_morphology_embeddings/DAY4.md`](day4_morphology_embeddings/DAY4.md)
for install notes and a graceful fallback if it isn't installed.

Any Jupyter/Colab environment works too — every experiment is a plain `.py` script
with clearly separated cells-by-comment, so copy-paste into notebook cells if preferred.

## A note on Indic-language tool support

Tool support is **not even** across the four languages used here, and that unevenness
is itself a teaching point, not a bug to route around:

- **NLTK / spaCy** were built English-first. spaCy has no official Malayalam or Tamil
  pipeline, and only a small Hindi one; NLTK's tokenizers are largely whitespace/
  punctuation heuristics that don't understand Indic conjuncts well.
- **Regex-based morphology** (prefix/suffix stripping) works reasonably for Hindi
  (less agglutinative) but breaks down fast on Malayalam and Tamil, where a single
  word can carry a chain of fused suffixes (case, tense, negation, number). Day 4
  makes this failure visible on purpose, then introduces FST-based analysis
  (`mlmorph` for Malayalam) as the real fix.
- **Subword tokenizers** (BPE/WordPiece/SentencePiece, Day 3) are the one modern tool
  that degrades gracefully across all four languages, which is exactly why Day 3
  uses them as a bridge into Day 4's morphology discussion.

Participants should come away knowing *which* tool is appropriate for *which*
language and task, not assuming any one library "just works" everywhere.

## Where to get real corpora

The sample data bundled here (`day1_python_basics_unicode/data/`, reused by every
later day) is small and hand-built, for teaching only. For real project work, point
participants to:

- Malayalam Wikipedia dump (dumps.wikimedia.org)
- AI4Bharat IndicCorp (multi-language, including Hindi, Tamil, Malayalam)
- Your own institution's corpora (e.g. ICFOSS's Malayalam corpora, where applicable)

Always check licensing before redistributing or publishing derived data.

## Extending this tutorial

This repo has a single maintainer (see above) — it is not open to outside pull
requests. It is, however, meant to accumulate more experiments over time, since the
intended audience is beginners who benefit from more worked examples, not fewer. To
add one:

1. Pick the day folder the concept belongs to (or propose a new day).
2. Add `expN_short_description.py` (next free number in that folder), following the
   existing scripts' style: a docstring header, section comments, and runnable
   top-to-bottom with `python3 expN_*.py`.
3. Reuse `day1_python_basics_unicode/data/` if the existing sample sentences fit;
   only add a new `data/` folder under your day if the experiment genuinely needs
   different data (keep it small — a dozen sentences per language is enough to
   teach a concept).
4. Add one line to the "Experiments" table in that day's `DAYx.md`.
5. If the experiment demonstrates a language-specific point, include at least
   English plus one Indic language; all four (English, Malayalam, Hindi, Tamil) where
   practical.

## License

Add your preferred license here before publishing (MIT/Apache-2.0 are common choices
for teaching material).
