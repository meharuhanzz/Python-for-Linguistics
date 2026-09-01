"""
Day 2, Experiment 2: Corpus analysis with pandas.

Concepts: DataFrame construction, groupby/value_counts, vocabulary size,
type-token ratio, sentence length.
Languages: English, Malayalam, Hindi, Tamil.

See library_notes/02_pandas.md for background before/while working through this.

Run: python3 exp2_pandas_corpus_analysis.py
"""

import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"
LANGUAGES = {"en": "English", "ml": "Malayalam", "hi": "Hindi", "ta": "Tamil"}
PUNCT_RE = re.compile(r"[.,!?;:।]")


def simple_tokenize(sentence: str) -> list[str]:
    cleaned = PUNCT_RE.sub("", sentence)
    return cleaned.split()


# ---------------------------------------------------------------------------
# Step 1: build one DataFrame covering all four languages -- one row per
# sentence, exactly the shape most real corpora arrive in.
# ---------------------------------------------------------------------------
rows = []
for code, name in LANGUAGES.items():
    path = DATA_DIR / f"sentences_{code}.txt"
    with open(path, encoding="utf-8") as f:
        for line in f:
            sentence = line.strip()
            if sentence:
                rows.append({"lang": code, "lang_name": name, "text": sentence})

df = pd.DataFrame(rows)
print("Corpus as a DataFrame:")
print(df.head(3))
print()


# ---------------------------------------------------------------------------
# Step 2: sentences per language -- a one-line answer thanks to value_counts.
# ---------------------------------------------------------------------------
print("Sentences per language:")
print(df["lang_name"].value_counts())
print()


# ---------------------------------------------------------------------------
# Step 3: derived columns -- token count and token list per sentence.
# ---------------------------------------------------------------------------
df["tokens"] = df["text"].apply(simple_tokenize)
df["n_tokens"] = df["tokens"].apply(len)

print("Average sentence length (tokens) per language:")
print(df.groupby("lang_name")["n_tokens"].mean().round(2))
print()


# ---------------------------------------------------------------------------
# Step 4: vocabulary size and type-token ratio (TTR) per language.
# TTR = unique words / total words -- higher means more lexical variety
# relative to corpus size. Comparing TTR *across* languages with this little
# data, and across languages with very different average word lengths, is a
# rough measure at best -- worth discussing, not just computing.
# ---------------------------------------------------------------------------
def vocab_stats(tokens_series: pd.Series) -> pd.Series:
    all_tokens = [tok for tokens in tokens_series for tok in tokens]
    vocab = set(all_tokens)
    ttr = len(vocab) / len(all_tokens) if all_tokens else 0.0
    return pd.Series({
        "total_tokens": len(all_tokens),
        "vocab_size": len(vocab),
        "type_token_ratio": round(ttr, 3),
    })


print("Vocabulary size and type-token ratio per language:")
print(df.groupby("lang_name")["tokens"].apply(vocab_stats).unstack())
print()
print("Caution: this sample corpus is tiny (8 sentences/language) and was")
print("hand-built for teaching, not sampled from real usage -- treat these")
print("numbers as a demonstration of the *method*, not a real finding.")
print()


# ---------------------------------------------------------------------------
# Step 5: filter rows containing a given (language-appropriate) word.
# ---------------------------------------------------------------------------
print("Sentences mentioning 'book' (English) or its Malayalam equivalent:")
mask = df["text"].str.contains("book", case=False) | df["text"].str.contains("പുസ്തകം")
print(df.loc[mask, ["lang_name", "text"]])


if __name__ == "__main__":
    pass
