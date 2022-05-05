from nltk.stem.porter import *
import nltk
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup

def convert_and_pad(word_dict, sentence, pad=500):
    NOWORD = 0
    INFREQ = 1

    working_sentence = [NOWORD] * pad

    for word_index, word in enumerate(sentence[:pad]):
        if word in word_dict:
            working_sentence[word_index] = word_dict[word]
        else:
            working_sentence[word_index] = INFREQ

    return working_sentence, min(len(sentence), pad)


def review_to_words(review):
    nltk.download("stopwords", quiet=True)
    stemmer = PorterStemmer()

    text = BeautifulSoup(review, "html.parser").get_text()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    words = text.split()
    words = [w for w in words if w not in stopwords.words("english")]
    words = [stemmer.stem(w) for w in words]

    return words