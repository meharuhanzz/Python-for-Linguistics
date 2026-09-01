"""
Day 3, Experiment 1: spaCy's full annotation pipeline on English.

Concepts: tokens, lemmas, POS tags, named entities, dependency relations.
Languages: English (spaCy has a mature trained pipeline for this).

See library_notes/03_spacy.md for background before/while working through this.

Setup (only needed once):
    python3 -m spacy download en_core_web_sm

Run: python3 exp1_spacy_pipeline_english.py
"""

from pathlib import Path

import spacy

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


nlp = spacy.load("en_core_web_sm")
en_sentences = load_sentences("en")


# ---------------------------------------------------------------------------
# Step 1: tokens, lemmas, POS tags -- one row per word.
# ---------------------------------------------------------------------------
example = en_sentences[-1]  # "The child read the book again."
doc = nlp(example)

print("=" * 60)
print(f"Full annotation for: {example!r}")
print("=" * 60)
print(f"{'TOKEN':<10}{'LEMMA':<10}{'POS':<8}{'DEP':<10}")
for token in doc:
    print(f"{token.text:<10}{token.lemma_:<10}{token.pos_:<8}{token.dep_:<10}")
print()


# ---------------------------------------------------------------------------
# Step 2: named entities.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Named entities across the English sample sentences")
print("=" * 60)
for sentence in en_sentences:
    d = nlp(sentence)
    if d.ents:
        for ent in d.ents:
            print(f"  {sentence!r} -> {ent.text!r} ({ent.label_})")
print()


# ---------------------------------------------------------------------------
# Step 3: dependency structure -- who is the subject, who is the object, and
# which word is the sentence's grammatical root.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Dependency relations (root, subject, object)")
print("=" * 60)
for sentence in en_sentences:
    d = nlp(sentence)
    root = [t for t in d if t.dep_ == "ROOT"][0]
    subjects = [t.text for t in d if t.dep_ in ("nsubj", "nsubjpass")]
    objects = [t.text for t in d if t.dep_ in ("dobj", "obj")]
    print(f"  {sentence!r}")
    print(f"    root={root.text!r}  subject={subjects}  object={objects}")


if __name__ == "__main__":
    pass
