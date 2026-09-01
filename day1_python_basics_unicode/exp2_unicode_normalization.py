"""
Day 1, Experiment 2: Unicode & Indic script handling.

Concepts: code points vs. grapheme clusters, NFC vs. NFD normalization,
ZWJ/ZWNJ inspection, why "identical-looking" strings can fail == .

See library_notes/00_python_stdlib_re_unicodedata.md for the background concepts
before/while working through this script.

Run: python3 exp2_unicode_normalization.py
"""

import unicodedata

# A Malayalam conjunct is a good example: ka+virama+sha is visually one glyph
# but is built from several separate Unicode code points.
malayalam_word = "ക്ഷമ"  # "patience"
hindi_word = "क्षमा"  # "forgiveness"
tamil_word = "க்ஷமா"  # "forgiveness"
english_word = "patience"


# ---------------------------------------------------------------------------
# Step 1: code points vs. what a human perceives as "one character".
# ---------------------------------------------------------------------------
print("How many 'characters' does Python count vs. what a human sees?\n")
for label, word in [
    ("English", english_word),
    ("Malayalam", malayalam_word),
    ("Hindi", hindi_word),
    ("Tamil", tamil_word),
]:
    print(f"{label}: {word!r}")
    print(f"  len() [code points]: {len(word)}")
    print(f"  code points        : {[hex(ord(c)) for c in word]}")
    print()


# ---------------------------------------------------------------------------
# Step 2: NFC vs. NFD normalization. The same visible text can be stored as
# either a small number of "precomposed" code points (NFC) or a larger number
# of "decomposed" base+combining-mark code points (NFD). Two files built by
# different tools can end up with the same *text* but different *bytes* --
# "café" is the textbook example: é can be one code point (U+00E9) or "e" +
# a combining acute accent (U+0301).
# ---------------------------------------------------------------------------
print("=" * 60)
print("NFC vs. NFD normalization")
print("=" * 60)

word = "café"
nfc = unicodedata.normalize("NFC", word)
nfd = unicodedata.normalize("NFD", word)

print(f"Word (as stored in this file): {word!r}")
print(f"NFC : {nfc!r}  (len={len(nfc)}, code points={[hex(ord(c)) for c in nfc]})")
print(f"NFD : {nfd!r}  (len={len(nfd)}, code points={[hex(ord(c)) for c in nfd]})")
print(f"NFC == NFD as raw strings? {nfc == nfd}")
print(f"After normalizing both sides to NFC, are they equal? "
      f"{unicodedata.normalize('NFC', nfc) == unicodedata.normalize('NFC', nfd)}")
print()
print("Lesson: never compare Unicode strings for equality -- or dedupe them, or")
print("use them as dict keys -- without normalizing both sides to the same form")
print("first. `unicodedata.normalize('NFC', text)` right after reading a file is")
print("the standard, safe default.")
print()
print("Gotcha specific to Hindi/Urdu-script text: nukta letters used to spell")
print("loanword sounds (e.g. Perso-Arabic 'q' as क़, ka+nukta) use a *compatibility*")
print("decomposition, not a canonical one -- so plain NFC/NFD leaves them alone,")
print("and you need unicodedata.normalize('NFKC', text) to fold them together.")
print()


# ---------------------------------------------------------------------------
# Step 3: Zero-Width Joiner (ZWJ, U+200D) and Zero-Width Non-Joiner
# (ZWNJ, U+200C) are invisible on screen but change rendering/meaning and will
# silently break naive tokenization or comparison if you don't know they're
# there. This is a very common source of "why doesn't my string match" bugs
# when working with real-world scraped Indic text.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Detecting invisible ZWJ / ZWNJ characters")
print("=" * 60)

ZWJ = "‍"
ZWNJ = "‌"

# "aan-kutti" (boy): aa (U+0D06) + chillu-n (U+0D7B) + kutti (child)
AA = "ആ"
CHILLU_N = "ൻ"  # MALAYALAM LETTER CHILLU N (U+0D7B)
KUTTI = "കുട്ടി"  # ku-tt-i


def find_invisible_chars(text: str) -> list[tuple[int, str]]:
    """Return (position, name) for any ZWJ/ZWNJ found in text."""
    hits = []
    for i, ch in enumerate(text):
        if ch == ZWJ:
            hits.append((i, "ZWJ (Zero-Width Joiner)"))
        elif ch == ZWNJ:
            hits.append((i, "ZWNJ (Zero-Width Non-Joiner)"))
    return hits


word_with_zwnj = AA + CHILLU_N + ZWNJ + KUTTI
word_without = AA + CHILLU_N + KUTTI

print(f"With ZWNJ   : {word_with_zwnj!r}")
print(f"Without ZWNJ: {word_without!r}")
print(f"Look the same when printed? -> {word_with_zwnj} vs {word_without}")
print(f"Are they equal as strings? {word_with_zwnj == word_without}")
print(f"Invisible characters found: {find_invisible_chars(word_with_zwnj)}")
print()
print("Lesson: two strings can render identically and still not be `==`. When")
print("corpus statistics look 'off' (a word appears twice with different counts),")
print("checking for ZWJ/ZWNJ and normalization mismatches is the first thing to try.")


if __name__ == "__main__":
    pass
