"""
Day 4, Experiment 1: where regex-based "morphology" breaks.

Concepts: suffix-matching false positives; why regex cannot distinguish a
real morphological suffix from a coincidentally-matching string ending,
without secretly encoding a lexicon of known stems.
Languages: Malayalam (locative suffix -il, -ിൽ), Tamil (dative suffix -kku,
-க்கு).

Run: python3 exp1_regex_morphology_limits.py
"""

import re

# ---------------------------------------------------------------------------
# Malayalam: the locative case suffix "-ിൽ" ("in X") is genuinely a suffix
# on nouns like വീട് (house) -> വീട്ടിൽ (in the house). But a regex matching
# "ends in ിൽ" cannot know that -- it will match ANY word with that letter
# sequence at the end, including a name or loanword where those letters are
# simply part of the word itself, not a case marker.
#
# The genuine examples are drawn from data/ (Day 1); the false-positive
# example is a constructed proper name, deliberately labelled as such, used
# only to illustrate the general risk (proper nouns/loanwords can end in the
# same letters as a case suffix by pure coincidence) -- not presented as a
# naturally-occurring corpus finding.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Malayalam: locative suffix '-ിൽ' -- genuine matches vs. a constructed")
print("false positive")
print("=" * 60)

genuine_locative = ["വീട്ടിൽ", "കേരളത്തിൽ", "യോഗത്തിൽ"]  # house/Kerala/meeting + -il
constructed_name = "ജിബിൽ"  # a constructed example name, NOT an attested word --
                              # used only to show the letters "ിൽ" can end a word
                              # that has nothing to do with locative case

test_words = genuine_locative + [constructed_name]
pattern = re.compile(r".*ിൽ$")

for word in test_words:
    matched = bool(pattern.match(word))
    print(f"  {word!r:<15} matches '-ിൽ' pattern: {matched}")

print()
print("The regex matches all four words identically -- it has no way to tell that")
print("the first three are genuinely stem+locative-suffix, while the fourth is a")
print("single, unanalyzable name that happens to end in the same two letters.")
print("Regex operates purely on character sequences; it has no model of what a")
print("valid Malayalam noun stem is, so it cannot reject the coincidental match.")
print()


# ---------------------------------------------------------------------------
# Tamil: the dative/allative suffix "-க்கு" ("to X") is a genuine suffix in
# words like வீடு (house) -> வீட்டுக்கு (to the house). "பாக்கு" (areca /
# betel nut) is a real, common, single-morpheme Tamil noun that happens to
# end in the same letters -- stripping "-க்கு" from it as if it were a
# dative suffix would incorrectly produce "பா", which is not the stem of
# "areca nut" at all.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Tamil: dative suffix '-க்கு' -- a genuine false positive")
print("=" * 60)

genuine_dative = ["வீட்டுக்கு"]  # house + dative/allative ("to the house")
real_false_positive = "பாக்கு"  # areca/betel nut -- a real, monomorphemic word

for word in genuine_dative + [real_false_positive]:
    matched = bool(pattern2 := re.match(r".*க்கு$", word))
    stripped = word[: -len("க்கு")] if matched else word
    print(f"  {word!r:<15} matches '-க்கு' pattern: {bool(matched)}  "
          f"naive strip -> {stripped!r}")

print()
print("Naively stripping '-க்கு' from 'பாக்கு' produces 'பா', which is not a stem")
print("meaning anything related to 'areca nut' -- the naive rule silently produces")
print("a wrong analysis instead of failing loudly, which is the more dangerous")
print("failure mode: a corpus-wide script using this rule would mislabel every")
print("occurrence of this word without any error or warning.")
print()
print("Day 4 Session 2 / exp2_fst_morphology_malayalam.py shows the correct tool")
print("for this: an FST-based analyzer that only accepts stem+suffix combinations")
print("that are actually valid in the language, instead of guessing from characters.")


if __name__ == "__main__":
    pass
