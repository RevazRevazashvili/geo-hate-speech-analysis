import joblib
import streamlit as st
from lime.lime_text import LimeTextExplainer

classes = ["Non-Hate Speech", "Hate Speech"]
stopwords = {
    "კი",
    "არა",
    "და",
    "რომ",
    "რადგან",
    "ის",
    "ეს",
    "რო",
    "მას",
    "მისი",
    "შენი",
    "ჩემი",
    "რად",
    "რატომ"
    "მერე",
    "ან",
    "აუ",
    "ამის",
    "იმის",
    "რომც",
    "ეე",
    "ეეე",
    "ხარ",
    "ვარ",
    "როგორც",
    "რაც",
    "როდესაც",
    "სადაც",
    "თუ",
    "რა",
    "რომელი",
    "რომლიც",
    "როდის",
    "რაღა",
    "მაგრამ",
    "არ",
    "აქ",
    "იქ",
    "შემდეგ",
    "სად",
    "მე",
    "შენ",
    "თქვენ",
    "მიერ",
    "ვინ",
    "როგორ",
    "თუნდაც",
    "რათა",
    "ისინი",
    "ვინც",
    "რატო",
}

# You can use this list in your Python code as needed.


def is_undecided_class(probability):
    return 0.35 < probability < 0.7


def predicted_class_color(prediction):
    return {"Hate Speech": "r", "Non-Hate Speech": "g", "Undecided": "yellow"}[prediction]


def get_influential_words(text, pipeline, num_features=10):
    # Create a LIME explainer
    explainer = LimeTextExplainer(
        kernel_width=25,
        kernel=None,
        verbose=False,
        class_names=classes,
        feature_selection='auto',
        split_expression='\W+',
        bow=True,
        mask_string=None,
        random_state=42,
        char_level=False
    )

    # Define a function to predict using your classifier
    predict_fn = lambda x: pipeline.predict_proba(x)

    try:
        # Explain the prediction for the given text
        explanation = explainer.explain_instance(text, predict_fn, num_features=num_features)

        # Get influential words and their importance scores
        influential_words = explanation.as_list()
        filtered_influential_words = [(word, score) for word, score in influential_words if word not in stopwords]
    except Exception as e:
        filtered_influential_words = []

    return filtered_influential_words


# load model, set cache to prevent reloading
@st.cache_resource(ttl=None, max_entries=1, show_spinner=True)
def load_model():
    model = joblib.load('models/tfidf_logreg_classifier.pkl')
    return model


def predict(text, model):
    pred = int(model.predict([text])[0])
    pred_proba = model.predict_proba([text])[0]
    pred_class = classes[pred]
    pred_probability = pred_proba[-1]
    influential_words = get_influential_words(text, model)
    hate_words = []
    non_hate_words = []
    if not is_undecided_class(pred_probability):
        if pred_class == classes[1]:
            hate_words = [(word, round(score, 3)) for word, score in influential_words if score > 0]
        else:
            non_hate_words = [(word, round(score, 3)) for word, score in influential_words if score < 0]

        return {
            "prediction": pred_class,
            "color": predicted_class_color(pred_class),
            "probability": pred_probability,
            "hate_words": hate_words,
            "non_hate_words": non_hate_words
        }
    else:
        return {
            "prediction": "Undecided",
            "color": predicted_class_color("Undecided"),
            "probability": pred_probability,
            "hate_words": hate_words,
            "non_hate_words": non_hate_words
        }
