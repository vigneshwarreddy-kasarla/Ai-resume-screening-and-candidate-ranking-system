from gensim.models import FastText
import numpy as np

def train_fasttext(sentences):
    # Remove empty token lists
    sentences = [s for s in sentences if len(s) > 0]

    if len(sentences) < 2:
        raise ValueError("Not enough valid text to train FastText.")

    model = FastText(
        vector_size=100,
        window=5,
        min_count=1,
        workers=4
    )

    model.build_vocab(sentences)
    model.train(sentences, total_examples=len(sentences), epochs=10)

    return model


def get_doc_vector(tokens, model):
    tokens = [t for t in tokens if t in model.wv]

    if not tokens:
        return np.zeros(100)

    vectors = [model.wv[t] for t in tokens]
    return np.mean(vectors, axis=0)
siddu