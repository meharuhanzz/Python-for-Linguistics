"""
Day 3, Experiment 3: subword tokenization compared across four languages.

Concepts: BPE/WordPiece subword tokenization, why token-piece count is a
rough statistical proxy for morphological complexity.
Languages: English, Malayalam, Hindi, Tamil, via one shared multilingual
tokenizer (MuRIL) so the comparison is apples-to-apples.

See library_notes/04_huggingface_tokenizers_transformers.md for background
before/while working through this.

First run downloads the tokenizer (~a few MB, not the full model weights).

Run: python3 exp3_subword_tokenization_comparison.py
"""

from pathlib import Path

from transformers import AutoTokenizer

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"
LANGUAGES = {"en": "English", "ml": "Malayalam", "hi": "Hindi", "ta": "Tamil"}


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


tokenizer = AutoTokenizer.from_pretrained("google/muril-base-cased")


# ---------------------------------------------------------------------------
# Step 1: tokenize one word per language and look at the actual pieces.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Subword pieces for one word per language")
print("=" * 60)
sample_words = {
    "en": "reads",           # read + 3rd-person -s
    "ml": "വായിക്കുന്നു",     # read + present-tense suffix ("reads")
    "hi": "पढ़ता",             # read + habitual/present suffix (masc.) ("reads")
    "ta": "படித்தது",         # read + past-tense suffix ("read", past)
}
for code, word in sample_words.items():
    pieces = tokenizer.tokenize(word)
    print(f"{LANGUAGES[code]:<10} {word!r:<20} -> {pieces}  ({len(pieces)} piece(s))")
print()
print("The English word stays a single whole-word piece -- 'reads' is common enough")
print("to have its own vocabulary entry. The Malayalam/Hindi/Tamil verb forms above")
print("all split into two pieces: roughly a stem piece and a suffix-shaped piece")
print("(prefixed '##' meaning 'continues the previous piece, not the start of a new")
print("word'). The tokenizer was never told about verb stems or tense suffixes --")
print("this split is a side effect of which whole strings were frequent enough in")
print("its training data to earn their own vocabulary entry, not a morphological")
print("analysis. It happens to land close to the real stem+suffix boundary here,")
print("which is exactly why it's a useful *statistical proxy* -- and exactly why")
print("Day 4 introduces an FST-based tool that gets the boundary right on purpose,")
print("not by accident.")
print()


# ---------------------------------------------------------------------------
# Step 2: average pieces-per-word across each language's full sample corpus.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Average subword pieces per word, across the sample corpus")
print("=" * 60)
for code, name in LANGUAGES.items():
    sentences = load_sentences(code)
    total_words = 0
    total_pieces = 0
    for sentence in sentences:
        for word in sentence.split():
            word = word.strip(".,!?;:।")
            if not word:
                continue
            pieces = tokenizer.tokenize(word)
            total_words += 1
            total_pieces += len(pieces)
    avg = total_pieces / total_words if total_words else 0.0
    print(f"  {name:<10} words={total_words:<4} pieces={total_pieces:<4} avg pieces/word={avg:.2f}")

print()
print("A higher average here is not a value judgement on the language -- it")
print("reflects that this tokenizer's vocabulary contains more whole-word entries")
print("for some languages/word-shapes than others, and that fused morphology makes")
print("a given surface word rarer as a *whole unit* even when its parts are common,")
print("even though the stem and each suffix individually are frequent. Day 4 makes")
print("this connection to morphology explicit, with a proper FST-based analysis.")


if __name__ == "__main__":
    pass
