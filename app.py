import streamlit as st
from wordcloud import WordCloud
from youtube_comments_parser import parse_comments
from hate_speech_classifier import predict

api_key = "AIzaSyAIq1qYxHW3Ig1Kj-RJmGE2oJKKfnip7mg"

st.title("Georgian Hate Speech Detector")
status_text = st.sidebar.empty()

youtube_video_url = st.text_input("Youtube Video URL")

hate_words = []
predictions = []
for comment in parse_comments(url=youtube_video_url):
    prediction = predict(comment)
    # st.write(comment)
    # st.write(prediction)
    predictions.append(prediction['prediction'])
    hate_words.extend(prediction['hate_words'])

if hate_words:
    hate_words_text = ' '.join(hate_words)
    wcl = WordCloud(font_path="fonts/bpg_glaho_sylfaen.ttf", width=800, height=400, background_color='white').generate(hate_words_text)
    st.image(wcl.to_array())

if predictions:
    st.bar_chart(data=predictions)

st.button("Re-run")