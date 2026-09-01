# pandas

```bash
pip install pandas
```

## Concept

pandas gives you a *table* (a `DataFrame`) as a first-class Python object — think of
it as a spreadsheet you control with code instead of a mouse. For corpus work this
matters because a corpus is naturally tabular: one row per sentence or document, one
column for the text, maybe columns for language, source, date, or annotation labels.
Once your corpus is a DataFrame, questions like "how many sentences per language?",
"what's the vocabulary size?", "sort by sentence length", or "filter to only rows
containing a given word" become one-line operations instead of hand-written loops.

The other reason pandas matters here: almost every real corpus you'll receive (a CSV
of annotated data, a spreadsheet of survey transcriptions, an export from an annotation
tool) arrives as a table, not as neatly pre-split Python lists. Learning to load and
manipulate that table directly, rather than converting it to lists first, is the more
transferable skill.

## Basic usage

```python
import pandas as pd

df = pd.DataFrame({
    "lang": ["en", "en", "ml", "ml"],
    "text": [
        "The boy went to the house.",
        "The girl reads a book.",
        "അവൻ വീട്ടിലേക്ക് പോയി.",
        "കുട്ടി പുസ്തകം വായിക്കുന്നു.",
    ],
})

print(df.head())

# how many sentences per language?
print(df["lang"].value_counts())

# add a column: sentence length in words
df["n_words"] = df["text"].str.split().str.len()
print(df.sort_values("n_words", ascending=False))

# filter: only rows mentioning a given word
print(df[df["text"].str.contains("book|പുസ്തകം")])
```

## Where this is used

Day 2's `exp2_pandas_corpus_analysis.py` — loading the 4-language sample corpus into
one DataFrame, computing per-language vocabulary size, type-token ratio, and sentence
length, all directly comparable across languages because they live in the same table.
