# spaCy

```bash
pip install spacy
python3 -m spacy download en_core_web_sm
```

## Concept

Where NLTK gives you separate building blocks you assemble yourself, spaCy gives you
one *pipeline*: feed it a sentence, and it comes back already tokenized, lemmatized
(reduced to dictionary form — "reads"/"reading"/"read" all map to "read"), POS-tagged
(noun, verb, adjective, ...), with named entities marked (person, place, organization),
and with a full dependency parse (which words grammatically depend on which — e.g.
"book" is the object of "reads"). It's the standard choice in applied NLP because it's
fast, production-oriented, and gives you all of these annotation layers from one call
instead of five separate tools.

The important limitation for this tutorial: spaCy's pipelines are trained per language
on large annotated treebanks, and no such trained pipeline currently exists for
Malayalam, Hindi, or Tamil — all three get only spaCy's basic rule-based "language
data" (tokenization rules, stopwords), not a statistical or neural model. So spaCy is
the right tool to *learn the concepts* of POS tagging and dependency parsing on
English, but not currently a tool you can point at any of these three languages and
expect the same quality — Day 3 demonstrates this gap directly rather than glossing
over it.

## Basic usage

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The child read the book again.")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)
# The   the    DET   det
# child child  NOUN  nsubj
# read  read   VERB  ROOT
# the   the    DET   det
# book  book   NOUN  dobj
# again again  ADV   advmod

for ent in doc.ents:
    print(ent.text, ent.label_)
```

## Where this is used

Day 3's `exp1_spacy_pipeline_english.py` runs the full pipeline on English sample
sentences; `exp2_spacy_limits_indic.py` shows what happens (and what still works, like
sentence splitting via a blank pipeline) when you point spaCy at Malayalam/Hindi/Tamil
text without a trained pipeline for that language.
