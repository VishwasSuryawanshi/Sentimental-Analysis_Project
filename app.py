import pickle
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import textblob
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import nltk
import re
import altair as alt

nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

port = PorterStemmer()


def text_cleaner(text):
    cleaned = re.sub('[^a-zA-Z]', " ", text)
    cleaned = cleaned.lower()
    cleaned = cleaned.split()
    cleaned = [port.stem(word) for word in cleaned if word not in stopwords.words("english")]
    cleaned = ' '.join(cleaned)
    return cleaned


def convert_to_df(sentiment):
    sentiment_dict = {'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity}
    sentiment_df = pd.DataFrame(sentiment_dict.items(), columns=['metric', 'value'])
    return sentiment_df


def analyze_token_sentiment(docx):
    analyzer = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []
    for i in docx.split():
        res = analyzer.polarity_scores(i)['compound']
        if res > 0.1:
            pos_list.append(i)
            pos_list.append(res)

        elif res <= -0.1:
            neg_list.append(i)
            neg_list.append(res)
        else:
            neu_list.append(i)

    result = {'positives': pos_list, 'negatives': neg_list, 'neutral': neu_list}
    return result


model = pickle.load(open("NLP_Model.pkl", "rb"))

st.title("Sentimental Analysis of Customer Review of a Product")
nav = st.sidebar.radio("Navigation", ["About Product", "Customer Review"])

if nav == "About Product":
    st.header("SJCAM -- Empower Your Dreams !!!")

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.image("sjcam.png", width=500)

    import streamlit as st
    import base64

    file_path = "D:\spec_sjcam.pdf"


    def show_pdf(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)


    show_pdf("spec_sjcam.pdf")

if nav == "Customer Review":
    input_review = st.text_area("Customer can write down their Review here : ")
    input_rating = st.slider("Choose a number for Rating", min_value=1, max_value=5)

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col1:
        st.empty()
    with col2:
        if input_rating == 1:
            st.markdown(":star:")
        if input_rating == 2:
            st.markdown(":star::star:")
        if input_rating == 3:
            st.markdown(":star::star::star:")
        if input_rating == 4:
            st.markdown(":star::star::star::star:")
        if input_rating == 5:
            st.markdown(":star::star::star::star::star:")
    with col3:
        st.empty()

    cv = CountVectorizer(binary=True)

    if st.button("Predict"):
        br = TextBlob(input_review)
        result = br.sentiment.polarity
        if result == 0:
            custom_emoji = ':smile:'
            st.success("This is a Neutral Massage")
        elif result > 0:
            custom_emoji = ':disappointed:'
            st.success("This is a Positive message")
        else:
            st.success("This is a Negative message")

        sentiment = TextBlob(input_review).sentiment
        # st.write(sentiment)

        # Emoji
        if sentiment.polarity > 0:
            st.markdown("Sentiment:: Positive :smiley: ")
        elif sentiment.polarity < 0:
            st.markdown("Sentiment:: Negative :angry: ")
        else:
            st.markdown("Sentiment:: Neutral 😐 ")

        # Dataframe
        result_df = convert_to_df(sentiment)
        st.dataframe(result_df)

        # Visualization
        c = alt.Chart(result_df).mark_bar().encode(
            x='metric',
            y='value',
            color='metric')
        st.altair_chart(c, use_container_width=True)

        st.info("Token Sentiment")

        token_sentiments = analyze_token_sentiment(input_review)
        st.write(token_sentiments)
