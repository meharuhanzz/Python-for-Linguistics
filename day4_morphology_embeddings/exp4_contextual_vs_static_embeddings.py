"""
Day 4, Experiment 4: static (Word2Vec) vs. contextual (transformer) embeddings.

Concepts: a static embedding gives one fixed vector per word type, blending
every sense/context it ever appeared in; a contextual embedding produces a
different vector depending on the surrounding sentence.
Languages: English (classic polysemy example: "bank"), then Malayalam,
Hindi, Tamil (case-marker sensitivity, reusing Day 1's sentence pairs).

See library_notes/05_gensim.md and library_notes/06_sentence_transformers.md
for background before/while working through this.

First run downloads a small pretrained model (~100MB).

Run: python3 exp4_contextual_vs_static_embeddings.py
"""

from pathlib import Path

from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer, util

DATA_DIR = Path(__file__).parent.parent / "day1_python_basics_unicode" / "data"


def load_sentences(lang_code: str) -> list[str]:
    path = DATA_DIR / f"sentences_{lang_code}.txt"
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# ---------------------------------------------------------------------------
# Step 1: the static-embedding limitation, made concrete with "bank" -- a
# textbook example of a word with two unrelated senses (riverbank vs.
# financial institution).
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 1: Word2Vec gives 'bank' exactly ONE vector, blending both senses")
print("=" * 60)

toy_sentences = [
    "he sat by the river bank and watched the water".split(),
    "the boat reached the bank of the river".split(),
    "she deposited money at the bank yesterday".split(),
    "the bank approved his loan application".split(),
    "the child read the book again".split(),  # unrelated filler, for variety
]
w2v = Word2Vec(toy_sentences, vector_size=20, window=3, min_count=1, epochs=200, seed=13)

bank_vector = w2v.wv["bank"]
print(f"model.wv['bank'] -> a single 20-dim vector: {bank_vector[:5].round(3)}...")
print("There is no way to ask this model for 'the vector of bank in sentence 1")
print("specifically' -- once training is done, the riverbank and financial-bank")
print("training examples have both already been blended into this one vector, and")
print("that information about which sentence contributed what is gone for good.")
print()


# ---------------------------------------------------------------------------
# Step 2: a contextual model gives "bank" a different vector depending on the
# sentence it's embedded in, and separates the two senses accordingly.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 2: a contextual model separates the two senses of 'bank'")
print("=" * 60)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

river_sent = "He sat by the river bank and watched the water flow."
river_sent2 = "The boat reached the muddy bank of the river."
money_sent = "She deposited her salary at the bank yesterday."
money_sent2 = "The bank approved his loan application this morning."

embeddings = model.encode([river_sent, river_sent2, money_sent, money_sent2])
sim_same_river = util.cos_sim(embeddings[0], embeddings[1]).item()
sim_same_money = util.cos_sim(embeddings[2], embeddings[3]).item()
sim_cross_sense = util.cos_sim(embeddings[0], embeddings[2]).item()

print(f"similarity(river-bank sentence, another river-bank sentence)  = {sim_same_river:.3f}")
print(f"similarity(money-bank sentence, another money-bank sentence)  = {sim_same_money:.3f}")
print(f"similarity(river-bank sentence, money-bank sentence)          = {sim_cross_sense:.3f}")
print()
print("Same-sense pairs score higher than the cross-sense pair -- the model is")
print("using surrounding context ('water', 'muddy' vs. 'deposited', 'loan') to")
print("represent 'bank' differently depending on which sense is actually meant,")
print("something a static Word2Vec vector structurally cannot do.")
print()


# ---------------------------------------------------------------------------
# Step 3: the same phenomenon, but for morphological context rather than
# lexical polysemy -- reusing Day 1's sentence pairs across all four
# languages. Sentence 0 = "went TO the house" (allative-like), sentence 1 =
# "is IN the house" (locative-like), sentence 4 = an unrelated sentence
# (rain in Kerala), used as a control.
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 3: sentence embeddings are sensitive to a case-marker difference,")
print("not just to shared vocabulary")
print("=" * 60)

for lang_code, lang_name in [("en", "English"), ("ml", "Malayalam"), ("hi", "Hindi"), ("ta", "Tamil")]:
    sentences = load_sentences(lang_code)
    to_house, in_house, unrelated = sentences[0], sentences[1], sentences[4]
    embs = model.encode([to_house, in_house, unrelated])
    sim_pair = util.cos_sim(embs[0], embs[1]).item()
    sim_ctrl_a = util.cos_sim(embs[0], embs[2]).item()
    sim_ctrl_b = util.cos_sim(embs[1], embs[2]).item()
    print(f"\n{lang_name}:")
    print(f"  A (went to house)  : {to_house!r}")
    print(f"  B (is in house)    : {in_house!r}")
    print(f"  C (unrelated)      : {unrelated!r}")
    print(f"  sim(A, B) = {sim_pair:.3f}   sim(A, C) = {sim_ctrl_a:.3f}   sim(B, C) = {sim_ctrl_b:.3f}")

print()
print("A and B share most of their words (subject, 'house') but differ in the case")
print("marker and verb -- sim(A, B) should sit well below 1.0 (they are NOT treated")
print("as identical) but clearly above sim(A, C) and sim(B, C) (they are still much")
print("closer to each other than to the unrelated sentence). This is the same kind")
print("of context-sensitivity as Step 2's 'bank' example, applied to a grammatical")
print("distinction instead of a lexical one -- directly relevant to why Day 4")
print("treats morphology and embeddings as connected topics, not separate ones.")


if __name__ == "__main__":
    pass
