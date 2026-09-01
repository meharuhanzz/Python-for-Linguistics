# Python standard library: `re` and `unicodedata`

No installation needed — both ship with Python itself.

## Concept

**`re` (regular expressions)** is a mini pattern-matching language for text. Instead
of writing a loop that checks each character by hand, you describe a *pattern*
("a word starting with a capital letter", "three digits in a row", "a word ending in
one of these three suffixes") and `re` finds every place that pattern occurs. In
linguistics, regex is the first tool for surface-level pattern search: finding all
words with a given prefix/suffix, extracting numbers or dates, splitting text on
punctuation. It has no understanding of *meaning* or *grammar* — it just matches
character patterns — which is both its strength (simple, fast, predictable) and its
limit (Day 4 shows exactly where that limit bites for agglutinative languages).

**`unicodedata`** answers questions about individual Unicode characters and lets you
*normalize* text. Text in any script is stored as a sequence of numbers (code points),
and for many scripts — Malayalam, Hindi, Tamil, and even accented Latin text like
"café" — the *same* visible text can be stored as different sequences of numbers. If
you don't normalize to one consistent form, two "identical" words can silently fail an
equality check, mess up your word-frequency counts, or break search. `unicodedata` is
how you detect and fix this.

## Basic usage

```python
import re

text = "The child read 3 books in 2024."

# find all sequences of digits
numbers = re.findall(r"\d+", text)
print(numbers)  # ['3', '2024']

# find words ending in a given suffix
words = ["played", "walked", "runs", "jumped"]
past_tense = [w for w in words if re.search(r"ed$", w)]
print(past_tense)  # ['played', 'walked', 'jumped']
```

```python
import unicodedata

word = "café"  # may be stored as 4 code points (é precomposed) or 5 (e + accent)

# always normalize right after reading text, before comparing/counting/storing
normalized = unicodedata.normalize("NFC", word)

# inspect what a character actually is
print(unicodedata.name("é"))  # 'LATIN SMALL LETTER E WITH ACUTE'
```

## Gotcha: `\b` (word boundary) and Indic combining marks

`\b` in `re` is defined in terms of `\w` (word characters), and Python's `\w` does
**not** count Unicode combining marks (categories Mn/Mc) as word characters — only
letters, digits, and underscore. Many Indic dependent vowel signs (matras) are
combining marks: Hindi `े` (U+0947) and Tamil `ு`/`ூ`/`ே` are common examples. A word
that *ends* in one of these signs — which is extremely common, since most Indic
syllables are consonant+vowel-sign — will not register a `\b` right after it:

```python
import re
re.findall(r"ने\b", "बच्चे ने किताब पढ़ी")   # -> []  (unexpected!)
re.findall(r"ने(?=\s|$)", "बच्चे ने किताब पढ़ी")  # -> ['ने']  (works)
```

The fix is to replace `\b` with an explicit lookahead for whatever actually follows a
word in your text (whitespace, punctuation, end of string), rather than relying on
`\b`'s letters-and-digits-only definition. This is the same family of issue as the
NFC/NFD and ZWJ/ZWNJ points above — Python's text-processing defaults were not
designed with Indic scripts as the primary case — just showing up in `re` instead of
`==`.

## Where this is used

Day 1's `exp1_basic_text_structures.py` and `exp2_unicode_normalization.py` build the
core habits (tokenize with `re`, normalize with `unicodedata` immediately after
reading a file) that every later day assumes you already have in place.
