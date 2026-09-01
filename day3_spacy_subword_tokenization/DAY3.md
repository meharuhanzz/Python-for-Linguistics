# Day 3 — spaCy Annotation Pipelines & Subword Tokenization

## Schedule

1. Recap Day 2, Day 3 goals
2. Session 1 — spaCy: Tokens, Lemmas, POS, NER, Dependencies (English)
3. Session 2 — Where spaCy's Language Coverage Ends (Indic languages)
4. Session 3 — Subword Tokenization: BPE / WordPiece / SentencePiece
5. Session 4 — Comparing Subword Splits Across Four Languages
6. Hands-on Lab — run and extend `exp1`, `exp2`, `exp3`
7. Wrap-up, Q&A, preview Day 4

## Learning objectives

By the end of Day 3, participants can:

- Run spaCy's full annotation pipeline on English text and read off tokens, lemmas,
  POS tags, named entities, and dependency relations.
- Explain, concretely, what happens (and what still works) when spaCy is pointed at a
  language it has no trained pipeline for.
- Explain what a subword tokenizer does differently from a whitespace tokenizer, and
  why that specifically matters for agglutinative languages.
- Compare token counts and splits for comparable sentences across English,
  Malayalam, Hindi, and Tamil using a real pretrained multilingual tokenizer.

## Session 1 — spaCy on English

The full pipeline in one call: `nlp(text)` returns a `Doc` with per-token attributes
(`.text`, `.lemma_`, `.pos_`, `.dep_`) and sentence/entity-level structure. See
`library_notes/03_spacy.md`.

## Session 2 — Where spaCy's Language Coverage Ends

spaCy has no official *trained* pipeline for Malayalam, Hindi, or Tamil — all three
only get spaCy's basic rule-based "language data" (tokenization rules, stopwords),
the same tier a `spacy.blank()` pipeline uses. This
session runs a **blank** spaCy pipeline (rule-based sentence boundaries and
whitespace tokenization only, with no statistical model) on Malayalam/Hindi/Tamil
sample sentences to show precisely what you still get "for free" (basic
tokenization/segmentation) versus what silently isn't there (POS tags, lemmas,
dependency parses — those attributes exist on the `Doc` object but are empty/default,
which is its own small trap for beginners who don't check).

## Session 3 — Subword Tokenization

BPE, WordPiece, and SentencePiece all solve the same problem — turning an open
vocabulary into a fixed-size set of frequent pieces — via slightly different
algorithms. The practical takeaway for this tutorial is behavioural, not
algorithmic: rare/long/morphologically complex words get split into multiple pieces
instead of becoming a single "unknown" token. See
`library_notes/04_huggingface_tokenizers_transformers.md`.

## Session 4 — Comparing Subword Splits Across Four Languages

Using one multilingual tokenizer (so the comparison is apples-to-apples), tokenize
comparable sentences in all four languages and count pieces per word. English words
mostly stay whole; Malayalam and Tamil words — carrying fused case/tense/negation
suffixes — split into noticeably more pieces on average. This sets up Day 4 directly:
subword splits are a *statistical* proxy for morphological complexity, not a
*linguistic* analysis of it — which is exactly the gap FST-based morphology (Day 4)
closes.

## Experiments

| Script | Demonstrates | Languages |
|---|---|---|
| `exp1_spacy_pipeline_english.py` | Full spaCy pipeline: tokens, lemmas, POS, NER, dependencies | English |
| `exp2_spacy_limits_indic.py` | Blank-pipeline fallback behaviour; what's missing without a trained model | Malayalam, Hindi, Tamil |
| `exp3_subword_tokenization_comparison.py` | Token-piece counts for comparable sentences via a multilingual subword tokenizer | English, Malayalam, Hindi, Tamil |

## Data

Reuses `day1_python_basics_unicode/data/sentences_*.txt`.

## Going further

- In `exp3`, try a monolingual English tokenizer (e.g. GPT-2's) on the Malayalam/Tamil
  sentences and compare piece counts against the multilingual tokenizer's. What
  happens to a tokenizer's behaviour on a script it was never trained on?
- Look up whether a Hindi spaCy pipeline (`xx_ent_wiki_sm` or a Hindi-specific model,
  depending on what's currently published) changes any of Session 2's results, and
  update `exp2` if so — tool coverage for these languages changes over time, which is
  itself worth tracking in this repo.
