import random

classes = ["Hate Speech", "Non-Hate Speech"]
genders = ["Male", "Female"]

def tokenize_text(text):
    return text.split(" ")

def get_hate_tokens(tokens):
    hate_tokens = []
    for token in tokens:
        if random.random() > 0.8:
            hate_tokens.append(token)

    return hate_tokens


def predict(text):
    if random.random() > 0.5:
        prediction = classes[1]
    else:
        prediction = classes[0]

    tokens = tokenize_text(text)
    hate_tokens = get_hate_tokens(tokens)

    return {"prediction": prediction, "hate_words": hate_tokens}



