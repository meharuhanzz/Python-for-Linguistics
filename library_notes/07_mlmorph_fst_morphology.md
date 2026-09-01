# `mlmorph` (FST-based Malayalam morphology) — optional deep-dive

This one is optional and Malayalam-specific: it's included because it's the correct
tool for the exact problem Day 4 raises (regex-based morphology breaking down on
agglutinative languages), not because every participant needs to install it to follow
the tutorial. If it isn't installed, `exp2_fst_morphology_malayalam.py` explains what
it *would* show and falls back to a smaller hand-built demonstration.

```bash
pip install mlmorph
```

## Concept

A **finite-state transducer (FST)** is a different kind of tool from regex: instead of
just matching a pattern, it's built from an actual model of a language's morphology
(which stems exist, which suffixes attach to which stems, what order they go in, what
grammatical feature each suffix marks) and can run in two directions — **analysis**
(take a surface word, return its stem + grammatical features) and **generation** (take
a stem + desired features, produce the correct surface word).

This is precisely what regex can't do. A regex suffix-strip rule like "remove trailing
-ിൽ" will match any word ending in those letters, whether or not that's genuinely a
locative case suffix on a real stem — it has no model of what stems or suffixes
actually exist in the language. An FST-based analyzer like `mlmorph` only accepts
combinations that are actually valid Malayalam morphology, and can *generate* a
correctly-inflected new form (e.g. take a word's locative form and produce its
allative form) — the regex approach cannot do this generation step at all.

## Basic usage

Analysis and generation are two separate classes:

```python
from mlmorph import Analyser, Generator

analyser = Analyser()
generator = Generator()

# analysis: surface word -> ranked list of (tag_string, weight) candidates,
# lower weight = more likely. Real analysers return many candidates because
# Malayalam has genuine structural ambiguity -- this is expected, not a bug.
candidates = analyser.analyse("വീട്ടിൽ")
print(sorted(candidates, key=lambda c: c[1])[:2])
# [('വീട്ടിൽ<np>', 134), ('വീട്<n><locative>', 166)]
# -> stem "വീട്" (house) + locative case is the second-ranked reading

# generation: stem + tags -> ranked list of (surface_form, weight) candidates
print(generator.generate("വീട്<n><genitive>")[0])
# ('വീടിന്റെ', ...)  -- "house's" / "of the house"
```

An invalid tag combination (e.g. a verb-tense tag on a noun) generates nothing at
all, rather than silently producing a wrong answer — this rejection-by-construction
is exactly what a regex-based approach cannot do.

## Where this is used

Day 4's `exp1_regex_morphology_limits.py` shows the regex approach failing/
over-matching; `exp2_fst_morphology_malayalam.py` shows the same task done correctly
with `mlmorph`, closing the loop on why this tutorial treats "morphology" and
"multimodal/multilingual NLP tooling" as connected topics rather than separate ones.
