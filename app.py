import streamlit as st
from wordcloud import WordCloud

from hate_speech_classifier import load_model, predict
from youtube_comments_parser import parse_comments

api_key = "AIzaSyAxAP3RT00cK0Y5RSDtE2Mma36IoFabY3c"

st.title("Georgian Hate Speech Detector")

model = load_model()

youtube_video_url = st.text_input(
    "Youtube Video URL",
    max_chars=200,
    value="https://www.youtube.com/watch?v=QvLsL6tjrcQ&ab_channel=MaroKalatozishvili%E2%80%A2AutoVlog"
)

max_comments = st.number_input(
    "Maximum Number Of Comments To Analyze",
    min_value=0,
    max_value=1000,
    value=10
)

hate_words = []
non_hate_words = []
predictions = []
for idx, comment in enumerate(parse_comments(url=youtube_video_url)):
    prediction = predict(text=comment, model=model)
    # st.write(comment)
    # st.write(prediction)
    predictions.append(prediction['prediction'])
    hate_words.extend(prediction['hate_words'])
    non_hate_words.extend(prediction['non_hate_words'])

    if idx + 1 == max_comments:
        break

if hate_words:
    hate_words_text = ' '.join(hate_words)
    wcl = WordCloud(font_path="fonts/bpg_glaho_sylfaen.ttf", width=800, height=400, background_color='white').generate(hate_words_text)
    st.image(image=wcl.to_array(), caption="Hate Speech Words")

if non_hate_words:
    non_hate_words_text = ' '.join(non_hate_words)
    wcl = WordCloud(font_path="fonts/bpg_glaho_sylfaen.ttf", width=800, height=400, background_color='white').generate(non_hate_words_text)
    st.image(image=wcl.to_array(), caption="Non-Hate Speech Words")

if predictions:
    st.bar_chart(data=predictions)

st.button("Re-run")