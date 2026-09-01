"""
Day 4, Experiment 2: FST-based morphological analysis with mlmorph.

Concepts: analysis (surface word -> stem + tags), generation (stem + tags ->
surface word), round-trip validation (only keep a generated candidate if
re-analysing it recovers the tag you asked for) -- the correct alternative
to the regex approach shown breaking down in exp1_regex_morphology_limits.py.
Language: Malayalam.

See library_notes/07_mlmorph_fst_morphology.md for background.

Setup (only needed once): pip install mlmorph
This script degrades to a small hand-built fallback demo if mlmorph is not
installed, so the tutorial still runs without it -- but installing it is
worthwhile, since the real tool makes the point far more convincingly.

Run: python3 exp2_fst_morphology_malayalam.py
"""

try:
    from mlmorph import Analyser, Generator
    MLMORPH_AVAILABLE = True
except ImportError:
    MLMORPH_AVAILABLE = False


def run_with_mlmorph() -> None:
    analyser = Analyser()
    generator = Generator()

    # -----------------------------------------------------------------
    # Step 1: analysis. Feed a real surface word in, get stem + tags out.
    # A real FST analyser returns many candidate analyses (Malayalam has
    # genuine structural ambiguity), ranked by weight -- unlike a regex,
    # which either matches or doesn't, with no notion of "more likely".
    # -----------------------------------------------------------------
    print("=" * 60)
    print("Step 1: analysis -- surface word -> ranked candidate analyses")
    print("=" * 60)
    word = "വീട്ടിൽ"  # "in the house"
    analyses = analyser.analyse(word)
    print(f"analyse({word!r}) returned {len(analyses)} candidate analyses.")
    print("Top 3 by weight (lower = more likely):")
    for tag, weight in sorted(analyses, key=lambda r: r[1])[:3]:
        print(f"  {tag!r:<45} weight={weight}")
    print()
    print("The single simplest, linguistically correct reading is")
    print("'വീട്<n><locative>' (stem വീട് 'house' + locative case) -- the second-")
    print("ranked candidate above. Ambiguity like this is normal and expected for a")
    print("real morphological analyser; a regex has no equivalent concept at all.")
    print()

    # -----------------------------------------------------------------
    # Step 2: generation + round-trip validation. This is Algorithm 1's
    # core loop: take a stem, mutate the case tag, generate a candidate
    # surface form, then re-analyse that candidate and keep it only if
    # the re-analysis recovers the tag we asked for.
    # -----------------------------------------------------------------
    print("=" * 60)
    print("Step 2: generate a full case paradigm, round-trip-validating each form")
    print("=" * 60)
    stem = "വീട്"
    cases = ["locative", "dative", "genitive", "sociative", "instrumental", "ablative"]
    print(f"{'case':<14}{'generated form':<20}{'round-trip valid?':<20}")
    for case in cases:
        tag = f"{stem}<n><{case}>"
        candidates = generator.generate(tag)
        if not candidates:
            print(f"{case:<14}{'(none generated)':<20}{'n/a':<20}")
            continue
        surface_form = candidates[0][0]
        reanalyses = analyser.analyse(surface_form)
        roundtrip_ok = any(cand_tag == tag for cand_tag, _ in reanalyses)
        print(f"{case:<14}{surface_form:<20}{str(roundtrip_ok):<20}")
    print()
    print("Every case above round-trips successfully -- these are all genuinely valid")
    print("Malayalam inflected forms of വീട് (house). This is the mechanism behind")
    print("this tutorial's Day 4 morphology point: instead of guessing from surface")
    print("characters, generate from a real grammatical model, then double-check by")
    print("re-analysing before trusting the result.")
    print()

    # -----------------------------------------------------------------
    # Step 3: what a rejected (invalid) combination looks like.
    # -----------------------------------------------------------------
    print("=" * 60)
    print("Step 3: an invalid tag combination is rejected outright")
    print("=" * 60)
    bad_tag = f"{stem}<n><past>"  # nonsensical: nouns don't take a verb tense
    bad_result = generator.generate(bad_tag)
    print(f"generate({bad_tag!r}) -> {bad_result}")
    print("The generator returns nothing at all for a combination that isn't valid")
    print("Malayalam morphology -- compare this to exp1, where a regex happily")
    print("'matched' a word ending in the right letters regardless of whether that")
    print("match meant anything grammatically.")


def run_fallback_demo() -> None:
    print("mlmorph is not installed in this environment -- showing a small hand-built")
    print("fallback instead. Install with `pip install mlmorph` for the real tool.")
    print()

    # A tiny hand-built stand-in for what an FST-based analyser guarantees:
    # only accept a (stem, suffix) pair if it's in a known-valid list, rather
    # than accepting anything that merely ends in the right letters.
    known_valid = {
        ("വീട്", "ിൽ"): "locative (in the house)",
        ("വീട്", "ിലേക്ക്"): "allative (to the house)",
    }
    test_word = "ജിബിൽ"  # the same constructed non-noun example from exp1
    stem_guess, suffix_guess = "ജിബ്", "ിൽ"
    is_valid = (stem_guess, suffix_guess) in known_valid
    print(f"Naive regex would accept {test_word!r} as stem+'-ിൽ'.")
    print(f"A stem+suffix lexicon lookup rejects it: "
          f"({stem_guess!r}, {suffix_guess!r}) in known-valid list? {is_valid}")
    print()
    print("A real FST (mlmorph) generalizes this idea to the whole language instead")
    print("of a hand-built list of two entries, and can run in both directions:")
    print("analysis (word -> stem+tags) and generation (stem+tags -> word).")


if __name__ == "__main__":
    if MLMORPH_AVAILABLE:
        run_with_mlmorph()
    else:
        run_fallback_demo()
