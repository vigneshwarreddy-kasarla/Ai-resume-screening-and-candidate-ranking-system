from gensim.models import FastText

def train_fasttext(sentences):
    if not sentences or len(sentences) == 0:
        raise ValueError("No text data found. 'sentences' list is empty.")

    # Filter out empty token lists
    sentences = [s for s in sentences if len(s) > 0]

    if len(sentences) == 0:
        raise ValueError("After cleaning, no valid sentences remain.")

    model = FastText(
        vector_size=100,
        window=5,
        min_count=1,
        workers=4
    )
    
    model.build_vocab(sentences)
    model.train(sentences, total_examples=len(sentences), epochs=10)

    return model
