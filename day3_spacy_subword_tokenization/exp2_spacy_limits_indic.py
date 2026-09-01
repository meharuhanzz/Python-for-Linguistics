"""
Day 3, Experiment 2: what spaCy gives you (and doesn't) without a trained
pipeline for the language.

Concepts: blank pipelines, rule-based sentence/word segmentation, why POS/
lemma/dependency attributes are empty without a trained statistical model.
Languages: Malayalam, Hindi, Tamil (spaCy has no official *trained* pipeline
for any of the three -- all three get only spaCy's basic rule-based
"language data", the same tier `spacy.blank()` uses).

See library_notes/03_spacy.md for background before/while working through this.

Run: python3 exp2_spacy_limits_indic.py
"""

from pathlib import Path

import spacy

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# spacy.blank("xx") builds a pipeline with NO trained model: no POS tagger, no
# lemmatizer, no parser, no NER. All you get is rule-based tokenization
# (mostly whitespace + a generic punctuation list) -- there is no
# language-specific linguistic knowledge in this pipeline at all.
nlp_blank = spacy.blank("xx")  # "xx" = spaCy's code for "multi-language / no model"

print("=" * 60)
print("A blank spaCy pipeline: what's there, and what's silently missing")
print("=" * 60)

for lang in ("ml", "hi", "ta"):
    sentence = load_sentences(lang)[0]
    doc = nlp_blank(sentence)
    print(f"\n{lang}: {sentence!r}")
    print(f"  tokens          : {[t.text for t in doc]}")
    print(f"  token.pos_      : {[t.pos_ for t in doc]}   <- all empty, no tagger loaded")
    print(f"  token.lemma_    : {[t.lemma_ for t in doc]}   <- same text back, no lemmatizer")
    print(f"  token.dep_      : {[t.dep_ for t in doc]}   <- all empty, no parser loaded")
    print(f"  doc.ents        : {doc.ents}   <- always empty, no NER model loaded")

print()
print("This is the trap for beginners: `token.pos_` and `token.dep_` don't raise an")
print("error on a blank pipeline -- they just silently return empty strings. Code")
print("that looks like it's doing POS tagging on Malayalam may run without any error")
print("and produce meaningless output. Always check `nlp.pipe_names` (below) to see")
print("what components are actually loaded before trusting their output.")
print()
print("nlp_blank.pipe_names ->", nlp_blank.pipe_names)
print("(compare: an nlp.pipe_names for en_core_web_sm includes 'tagger', 'parser',")
print(" 'lemmatizer', 'ner' -- Day 3's exp1 uses exactly that pipeline.)")


if __name__ == "__main__":
    pass
