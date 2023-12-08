import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from hate_speech_classifier import load_model, predict
from youtube_comments_parser import parse_comments

api_key = st.secrets.credentials.api_key

st.title("ქართულენოვანი სიძულვილის ენის დეტექტორი")

model = load_model()

with st.form('input'):
    youtube_video_url = st.text_input(
        "ოუთუბის ვიდეოს ბმული",
        max_chars=1000,
        value="https://www.youtube.com/watch?v=QvLsL6tjrcQ&ab_channel=MaroKalatozishvili%E2%80%A2AutoVlog"
    )

    max_comments = st.number_input(
        "გასაანალიზებელი კომენტარების დაოდენობა",
        min_value=0,
        max_value=1000,
        value=10
    )

    submit_button = st.form_submit_button(label='გააანალიზე')


if submit_button:
    if not youtube_video_url.strip() or not max_comments:
        st.error('გთხოვთ შეავსოთ გამოტოვებული ველები!')
    else:
        with st.spinner(text='მიმდინარეობს მონაცემთა ანალიზი…'):
            hate_words = []
            non_hate_words = []
            predictions = []
            colors = []
            probabilities = []
            data = []
            for idx, comment in enumerate(parse_comments(url=youtube_video_url)):
                prediction = predict(text=comment, model=model)
                predictions.append(prediction['prediction'])
                colors.append(prediction['color'])
                probabilities.append(prediction['probability'])
                hate_words.extend(prediction['hate_words'])
                non_hate_words.extend(prediction['non_hate_words'])

                if idx + 1 == max_comments:
                    break

                data.append(
                    {
                        "კომენტარი": comment,
                        "კატეგორია": prediction['prediction'],
                        "ალბათობა": prediction['probability'],
                        "მნიშვნელოვანი სიტყვები": prediction['hate_words'] or prediction['non_hate_words'],
                    }
                )

            if hate_words:
                hate_words_text = ' '.join([word for word, score in hate_words])
                wcl = WordCloud(font_path="fonts/bpg_glaho_sylfaen.ttf", width=800, height=400, background_color='gray',
                                colormap="Reds").generate(hate_words_text)
                st.image(image=wcl.to_array(), caption="სიძულვილის ენა")

            if non_hate_words:
                non_hate_words_text = ' '.join([word for word, score in non_hate_words])
                wcl = WordCloud(font_path="fonts/bpg_glaho_sylfaen.ttf", width=800, height=400,
                                background_color='white',
                                colormap="summer").generate(non_hate_words_text)
                st.image(image=wcl.to_array(), caption="ბულბულის ენა")

            if predictions:
                st.bar_chart(data=predictions)

            st.download_button("გადმოწერა", data=pd.DataFrame(data).to_csv(), mime="text/csv")
