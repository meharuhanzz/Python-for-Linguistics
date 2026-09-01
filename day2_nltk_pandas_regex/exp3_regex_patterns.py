"""
Day 2, Experiment 3: Regular expressions for linguistic patterns.

Concepts: prefix/suffix matching, numeral extraction, a first (deliberately
naive) attempt at spotting a morphological case marker with regex.
Languages: English, Malayalam, Hindi, Tamil.

See library_notes/00_python_stdlib_re_unicodedata.md for the `re` background.
This experiment's last section is intentionally a *cautionary* demo -- Day 4
("Regex vs. FST-based morphology") returns to this exact problem in depth.

Run: python3 exp3_regex_patterns.py
"""

import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# ---------------------------------------------------------------------------
# Step 1: find English words ending in "-ed" (a common, if imperfect, way to
# spot past-tense verbs by surface form alone).
# ---------------------------------------------------------------------------
print("=" * 60)
print("English: words ending in '-ed'")
print("=" * 60)
en_text = " ".join(load_sentences("en"))
past_tense_like = re.findall(r"\b\w+ed\b", en_text)
print("Matches:", past_tense_like)
print("Note: this pattern would also match a noun that happens to end in -ed,")
print("e.g. 'shed' or 'bed' -- regex matches surface form, not grammar.")
print()


# ---------------------------------------------------------------------------
# Step 2: extract all numerals from a mixed sample (works identically for
# any of the four languages, since digits are shared across scripts here).
# ---------------------------------------------------------------------------
print("=" * 60)
print("Extracting numerals (script-independent)")
print("=" * 60)
mixed_sample = "The child read 3 books. In 2024, it rained for 15 days."
print("Text:", mixed_sample)
print("Numbers found:", re.findall(r"\d+", mixed_sample))
print()


# ---------------------------------------------------------------------------
# Step 3: find repeated words across the English sample corpus -- a common
# real task (e.g. spotting duplicate/boilerplate sentences in scraped data).
# ---------------------------------------------------------------------------
print("=" * 60)
print("Words repeated within the same sentence")
print("=" * 60)
for sentence in load_sentences("en"):
    repeats = re.findall(r"\b(\w+)\b(?=.*\b\1\b)", sentence, flags=re.IGNORECASE)
    if repeats:
        print(f"  {sentence!r} -> repeated: {set(w.lower() for w in repeats)}")
print()


# ---------------------------------------------------------------------------
# Step 4: a naive attempt at spotting a Malayalam locative case marker
# ("-ിൽ", "in X") purely by suffix string match. This is a DELIBERATE
# cautionary example: it will over-match, because regex has no concept of
# "is this actually a case suffix on a real noun stem" -- it just matches
# the literal character sequence "ിൽ" wherever it occurs, including inside
# words where those letters are part of the stem itself, not a suffix.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Naive suffix-based 'case marker' search (Malayalam) -- and why it fails")
print("=" * 60)
ml_text = " ".join(load_sentences("ml"))
locative_like = re.findall(r"\S*ിൽ\b", ml_text)
print(f"Words ending in '-ിൽ' found: {locative_like}")
print()
print("Some of these are genuinely locative-case nouns (a real suffix). Others may")
print("just be words that happen to end in that letter sequence for unrelated")
print("reasons -- regex cannot tell the difference, because it has no model of")
print("Malayalam word structure, only of character patterns. Day 4 shows the")
print("correct tool for this task: FST-based morphological analysis (mlmorph),")
print("which knows the actual stem+suffix structure instead of guessing from")
print("surface characters.")


if __name__ == "__main__":
    pass
