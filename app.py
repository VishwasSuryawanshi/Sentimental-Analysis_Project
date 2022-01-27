import pickle
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import re

nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from afinn import Afinn

af = Afinn(language="en", emoticons=False, word_boundary=True)

port = PorterStemmer()


def text_cleaner(text):
    cleaned = re.sub('[^a-zA-Z]', " ", text)
    cleaned = cleaned.lower()
    cleaned = cleaned.split()
    cleaned = [port.stem(word) for word in cleaned if word not in stopwords.words("english")]
    cleaned = ' '.join(cleaned)
    return cleaned


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
        try:
            if len([input_review]) > 2:
                cleaned_review = text_cleaner(input_review)
                cv_r = cv.transform([cleaned_review])
                result = model.predict(cv_r)
                if result == 1:
                    st.image("happy.png", width=70)
                    st.header("Hey, its Positive Review !!!")
                    st.header("Great, Keep it up")
                else:
                    st.image("sad.png", width=50)
                    st.header("Sadly, its Negative Review!")
                    st.header("There is scope for improvement")
            else:
                lst = input_review.split()
                if len(lst) == 1:
                    score = af.score(lst[0].lower())
                else:
                    for word in (lst):
                        if lst[0].lower() == "not":
                            score = af.score(lst[1]) * (-1)
                        else:
                            score = af.score(lst[0]) + (af.score(lst[1]))
                if score >= 0:
                    st.image("happy.png", width=70)
                    st.header("Hey, its Positive Review !!!")
                    st.header("Great, Keep it up")
                else:
                    st.image("sad.png", width=50)
                    st.header("Sadly, its Negative Review!!!")
                    st.header("There is scope for improvement")

        except:
            pass
