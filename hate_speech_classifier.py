import joblib
import streamlit as st
from lime.lime_text import LimeTextExplainer

classes = ["Non-Hate Speech", "Hate Speech"]
genders = ["Male", "Female"]


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
    except Exception as e:
        influential_words = []

    return influential_words


# load model, set cache to prevent reloading
@st.cache_resource(ttl=None, max_entries=1, show_spinner=True)
def load_model():
    model = joblib.load('models/tfidf_logreg_classifier.pkl')
    return model


def predict(text, model):
    pred = int(model.predict([text])[0])
    # print(text, pred, model.predict_proba([text]))
    pred_class = classes[pred]
    influential_words = get_influential_words(text, model)
    hate_words = []
    non_hate_words = []
    if pred_class == classes[1]:
        hate_words = [word for word, score in influential_words if score > 0]
    else:
        non_hate_words = [word for word, score in influential_words if score < 0]

    return {"prediction": pred_class, "hate_words": hate_words, "non_hate_words": non_hate_words}
