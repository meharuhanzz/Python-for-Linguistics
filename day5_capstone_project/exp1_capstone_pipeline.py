"""
Day 5, Experiment 1: capstone pipeline combining Days 1-4.

Concepts: everything in this tutorial, chained into one pipeline: load (Day
1/2) -> tokenize (Day 2/3) -> frequency/vocab stats (Day 2) -> regex search
(Day 2/4) -> deepest available annotation (spaCy for English, mlmorph FST
for Malayalam; Day 3/4) -> shared multilingual embeddings + cross-lingual
similarity search (Day 4).
Languages: English, Malayalam, Hindi, Tamil.

Run: python3 exp1_capstone_pipeline.py
"""

import re
from pathlib import Path

import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer, util

try:
    from mlmorph import Analyser
    MLMORPH_AVAILABLE = True
except ImportError:
    MLMORPH_AVAILABLE = False

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"
LANGUAGES = {"en": "English", "ml": "Malayalam", "hi": "Hindi", "ta": "Tamil"}
PUNCT_RE = re.compile(r"[.,!?;:।]")


def simple_tokenize(sentence: str) -> list[str]:
    return PUNCT_RE.sub("", sentence).split()


# ===========================================================================
# Step 1 (Day 2): load every language into one DataFrame.
# ===========================================================================
rows = []
for code, name in LANGUAGES.items():
    path = DATA_DIR / f"sentences_{code}.txt"
    with open(path, encoding="utf-8") as f:
        for line in f:
            sentence = line.strip()
            if sentence:
                rows.append({"lang": code, "lang_name": name, "text": sentence})
df = pd.DataFrame(rows)
df["tokens"] = df["text"].apply(simple_tokenize)
df["n_tokens"] = df["tokens"].apply(len)

print("#" * 70)
print("STEP 1 (Day 2): corpus loaded")
print("#" * 70)
print(df.groupby("lang_name")["n_tokens"].agg(["count", "mean"]).round(2))
print()


# ===========================================================================
# Step 2 (Day 2/4): a regex pattern search, per language.
# One illustrative pattern per language, reusing Day 2/4's case-marker theme.
# ===========================================================================
print("#" * 70)
print("STEP 2 (Day 2/4): regex pattern search")
print("#" * 70)
# Note: \b ("word boundary") is unreliable right after an Indic dependent
# vowel sign or virama -- Python's \w only counts Unicode category Lo/Nd/etc,
# NOT combining marks (categories Mn/Mc), so a word ending in a vowel sign
# (e.g. Hindi "ने", Tamil "க்கு") doesn't register a \b after it. We use an
# explicit "followed by whitespace/punctuation/end-of-string" lookahead
# instead -- this is the same family of Unicode gotcha as Day 1's
# NFC/NFD and ZWJ/ZWNJ discussion, just showing up in `re` instead of `==`.
END = r"(?=[\s.,!?;:।]|$)"
PATTERNS = {
    "en": r"\b\w+ed\b",              # past-tense-shaped words
    "ml": r"\S*ിൽ" + END,           # locative-suffix-shaped words
    "hi": r"\S*ने" + END,            # ergative-marker-shaped words
    "ta": r"\S*க்கு" + END,          # dative-suffix-shaped words
}
for code, name in LANGUAGES.items():
    text = " ".join(df.loc[df["lang"] == code, "text"])
    matches = re.findall(PATTERNS[code], text)
    print(f"  {name:<10} pattern={PATTERNS[code]!r:<25} matches={matches}")
print("(As Day 4 discussed: these are surface-pattern matches, not verified")
print("morphological analyses -- Step 4 below applies a real analyser for Malayalam.)")
print()


# ===========================================================================
# Step 3 (Day 3): deepest annotation available -- spaCy's full pipeline for
# English.
# ===========================================================================
print("#" * 70)
print("STEP 3 (Day 3): spaCy annotation (English)")
print("#" * 70)
nlp = spacy.load("en_core_web_sm")
en_example = df.loc[df["lang"] == "en", "text"].iloc[-1]
doc = nlp(en_example)
print(f"Sentence: {en_example!r}")
for token in doc:
    print(f"  {token.text:<10} lemma={token.lemma_:<10} pos={token.pos_:<8} dep={token.dep_}")
print()


# ===========================================================================
# Step 4 (Day 4): deepest annotation available -- FST-based morphological
# analysis for Malayalam, with a graceful fallback if mlmorph isn't
# installed.
# ===========================================================================
print("#" * 70)
print("STEP 4 (Day 4): FST-based morphological analysis (Malayalam)")
print("#" * 70)
ml_example = df.loc[df["lang"] == "ml", "text"].iloc[0]
print(f"Sentence: {ml_example!r}")
if MLMORPH_AVAILABLE:
    analyser = Analyser()
    for word in simple_tokenize(ml_example):
        analyses = analyser.analyse(word)
        if not analyses:
            print(f"  {word:<15} -> no analysis found")
            continue
        best_tag, best_weight = min(analyses, key=lambda r: r[1])
        print(f"  {word:<15} -> {best_tag}  (weight={best_weight})")
else:
    print("  mlmorph not installed -- run `pip install mlmorph` for this step.")
    print("  See day4_morphology_embeddings/exp2_fst_morphology_malayalam.py for")
    print("  what this step demonstrates once it's installed.")
print()
print("A 'no analysis found' result (if you see one above) is itself a real,")
print("meaningful outcome -- it means this particular surface form isn't covered by")
print("the analyser's current lexicon/rules, not that the script is broken. Real FST")
print("tools have coverage gaps like any other resource; silently returning nothing")
print("for an unrecognized word is safer than a regex-style false match (Step 2).")
print()


# ===========================================================================
# Step 5 (Day 4): shared multilingual embeddings + cross-lingual similarity
# search -- the capstone-only step that ties every language and every
# earlier day together into one demonstration.
# ===========================================================================
print("#" * 70)
print("STEP 5 (Day 4): cross-lingual similarity search")
print("#" * 70)
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
df["embedding"] = list(model.encode(df["text"].tolist()))

query_lang, query_text = "en", "It rained in Kerala."
query_embedding = model.encode(query_text)

print(f"Query ({LANGUAGES[query_lang]}): {query_text!r}")
print("Most similar sentence in each OTHER language:")
for code, name in LANGUAGES.items():
    if code == query_lang:
        continue
    candidates = df[df["lang"] == code]
    sims = util.cos_sim(query_embedding, list(candidates["embedding"]))[0]
    best_idx = sims.argmax().item()
    best_row = candidates.iloc[best_idx]
    print(f"  {name:<10} ({sims[best_idx].item():.3f}) -> {best_row['text']!r}")
print()
print("This is a small-scale version of cross-lingual information retrieval: finding")
print("the closest-meaning sentence in a DIFFERENT language, using no translation")
print("step at all -- just one shared embedding space that all four languages were")
print("encoded into. This is the same mechanism Day 4 introduced for within-language")
print("context sensitivity, applied here across languages instead.")


if __name__ == "__main__":
    pass
