"""
Day 4, Experiment 3: training a small Word2Vec model and inspecting its
vectors.

Concepts: static word embeddings, nearest-neighbour retrieval, why a bigger/
more repetitive corpus than Day 1's 8-sentence samples is needed for
Word2Vec to learn anything at all.
Languages: English, Malayalam, Hindi, Tamil (separate toy corpora, built
inline below since Word2Vec needs more repetition than the shared sample
data provides).

See library_notes/05_gensim.md for background before/while working through
this.

Run: python3 exp3_word2vec_gensim.py
"""

from gensim.models import Word2Vec

# ---------------------------------------------------------------------------
# Build small toy corpora with deliberate repetition, so that Word2Vec's
# co-occurrence statistics have something to learn from. These sentences are
# templated for grammatical consistency (e.g. Hindi/Tamil verb agreement is
# handled explicitly below, not by blind cross-product) -- they are still far
# too small to produce production-quality embeddings; the point is to watch
# the *mechanics* work, not to get meaningful similarities.
# ---------------------------------------------------------------------------

# English: no agreement to worry about, so a full cross-product is safe.
en_subjects = ["the child", "the boy", "the girl", "the man", "the woman"]
en_objects = ["book", "newspaper", "story", "letter"]
en_sentences = [
    f"the {s.split()[-1]} read the {o}".split()
    for s in en_subjects for o in en_objects
]

# Malayalam: the verb doesn't inflect for subject gender/number, so a full
# cross-product is also safe here.
ml_subjects = ["കുട്ടി", "ആൺകുട്ടി", "പെൺകുട്ടി", "മനുഷ്യൻ", "സ്ത്രീ"]
ml_objects = ["പുസ്തകം", "പത്രം", "കഥ", "കത്ത്"]
ml_sentences = [f"{s} {o} വായിച്ചു".split() for s in ml_subjects for o in ml_objects]

# Tamil: the verb DOES agree with the subject, so subject and verb form are
# paired explicitly rather than cross-producted freely.
ta_subject_verb = [("குழந்தை", "படித்தது"), ("சிறுவன்", "படித்தான்"), ("சிறுமி", "படித்தாள்")]
ta_objects = ["புத்தகம்", "செய்தித்தாள்", "கதை", "கடிதம்"]
ta_sentences = [
    f"{subj} {o} {verb}".split() for subj, verb in ta_subject_verb for o in ta_objects
]

# Hindi: in the perfective "ne"-ergative construction, the verb agrees with
# the OBJECT's gender, not the subject -- so object and verb form are paired
# explicitly, and subjects (which don't affect verb form here) vary freely.
hi_subjects = ["बच्चे ने", "लड़के ने", "लड़की ने"]
hi_object_verb = [("किताब", "पढ़ी"), ("अखबार", "पढ़ा"), ("कहानी", "पढ़ी"), ("पत्र", "पढ़ा")]
hi_sentences = [
    f"{subj} {o} {verb}".split() for subj in hi_subjects for o, verb in hi_object_verb
]

CORPORA = {
    "English": (en_sentences, "book"),
    "Malayalam": (ml_sentences, "പുസ്തകം"),
    "Tamil": (ta_sentences, "புத்தகம்"),
    "Hindi": (hi_sentences, "किताब"),
}


# ---------------------------------------------------------------------------
# Train one small model per language and inspect nearest neighbours of the
# word for "book" in each.
# ---------------------------------------------------------------------------
for lang, (sentences, query_word) in CORPORA.items():
    print("=" * 60)
    print(f"{lang}: {len(sentences)} toy sentences")
    print("=" * 60)

    model = Word2Vec(
        sentences, vector_size=20, window=3, min_count=1, epochs=200, seed=13
    )

    vector = model.wv[query_word]
    print(f"Vector for {query_word!r}: shape={vector.shape}, first 5 values={vector[:5].round(3)}")

    neighbours = model.wv.most_similar(query_word, topn=3)
    print(f"Words most similar to {query_word!r}: {neighbours}")
    print()

print("These similarities are trained on only a dozen or two sentences -- they")
print("demonstrate that the mechanism works (vectors exist, similarity is")
print("computable), not that the resulting embeddings are linguistically")
print("meaningful. Real Word2Vec training uses millions of sentences.")
print()
print("The more important limitation, covered next in")
print("exp4_contextual_vs_static_embeddings.py: every one of these models gives")
print(f"each word exactly ONE vector, no matter what sentence it appears in.")


if __name__ == "__main__":
    pass
