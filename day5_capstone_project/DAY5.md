# Day 5 — Mini Linguistic Data Project & Research Applications

## Schedule

1. Recap Days 1–4, Day 5 goals
2. Session 1 — Planning a Data Pipeline End to End
3. Session 2 — Capstone Lab, Part 1: Load, Tokenize, Frequencies
4. Session 3 — Capstone Lab, Part 2: Regex, POS/Morphology, Embeddings
5. Session 4 — Capstone Lab, Part 3: Cross-Lingual Similarity Search
6. Presentations — each participant/pair walks through their pipeline's output
7. Wrap-up — research applications, where to go next, Q&A

## Learning objectives

By the end of Day 5, participants can:

- Combine pandas, tokenization, regex, POS/morphological annotation, and embeddings
  into a single coherent pipeline over a multilingual corpus.
- Explain, for their own pipeline, which tool they chose at each stage and why
  (referring back to Days 1–4's language-coverage discussions rather than reaching
  for a tool out of habit).
- Run a simple cross-lingual similarity search using a shared multilingual embedding
  space.
- Describe at least two research applications (corpus building, annotation projects,
  morphological analysis, dialectology, translation studies, etc.) where this kind of
  pipeline is directly useful, and what would need to change to scale it beyond a
  teaching-sized sample corpus.

## Session 1 — Planning a Data Pipeline End to End

Before writing code: given a research question (e.g. "how does case-marker usage
differ between formal and spoken registers?"), what does the pipeline from raw text
to an answerable statistic actually look like? This session sketches that on the
board/collaboratively before Session 2 turns it into running code.

## Sessions 2–4 — Capstone Lab

Run `exp1_capstone_pipeline.py`, which walks through, per language:

1. Load the corpus into a pandas DataFrame (Day 2).
2. Tokenize (NLTK for English; a language-appropriate simple tokenizer otherwise, per
   Day 2/3's discussion of where NLTK's/spaCy's English-trained tools do and don't
   generalize).
3. Compute frequency and vocabulary statistics (Day 2).
4. Run a regex pattern search (Day 2/4).
5. Run the deepest annotation available for that language: spaCy's full pipeline for
   English, `mlmorph` FST analysis for Malayalam (Day 3/4).
6. Encode every sentence with a shared multilingual embedding model and run a
   cross-lingual similarity search: given a query sentence in one language, find the
   closest sentence *in any of the other three languages* (Day 4) — a capstone-only
   step that ties every earlier day together into one runnable demonstration.

Work through the script section by section rather than running it end to end
immediately — pause at each step and check the output makes sense before moving on.

## Experiments

| Script | Demonstrates | Languages |
|---|---|---|
| `exp1_capstone_pipeline.py` | The full Day 1–4 toolchain applied end to end, plus cross-lingual similarity search | English, Malayalam, Hindi, Tamil |

## Data

Reuses `day1_python_basics_unicode/data/sentences_*.txt` — the same corpus used
throughout the whole tutorial, so participants can see the full arc from "eight raw
sentences" (Day 1) to "a queryable, cross-lingual, annotated dataset" (Day 5).

## Research applications (for the closing discussion)

- **Corpus building**: this pipeline's shape (load → clean/normalize → tokenize →
  annotate → store) is the same shape as any real corpus-building project; only the
  scale and annotation depth change.
- **Annotation projects**: knowing which tool actually has coverage for your target
  language (Days 2–3) prevents wasted effort building an annotation pipeline around a
  tool that silently does nothing useful for that language (Day 3's blank-pipeline
  trap).
- **Morphological analysis / dialectology / historical linguistics**: FST-based tools
  like `mlmorph` (Day 4) generalize to any language with a comparable finite-state
  resource — the method, not just this specific tool, transfers.
- **Cross-lingual / translation studies**: the Session 4 similarity search is a small
  version of the technique behind cross-lingual information retrieval and parallel
  corpus mining.

## Where to go from here

- Scale up: point this same pipeline at a real corpus (Malayalam Wikipedia, IndicCorp,
  or your own collected data) instead of the 8-sentence teaching sample.
- Depth: pick one day's topic (morphology is the natural choice, given `mlmorph`) and
  go deeper than this tutorial's scope — e.g. building a small morphology-aware
  evaluation set for a task you care about.
- Contribute back: if you build something reusable while doing either of the above,
  consider whether a trimmed-down version belongs in this repo's later days as a new
  experiment (see the top-level README's "Extending this tutorial" section) — even
  though this repo has a single maintainer, sharing a script or a write-up with them is
  still how it grows.
