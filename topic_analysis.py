# !/usr/bin/env python
# coding: utf-8

# web scraping imports
from CNN import *

# install nltk, selenium, genism and bs4
# install chromedriver and add to path

# ntlk imports
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# prettyprint
import pprint

# genism imports
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

stopwords = []  # user defined stopwords


def process_article(text):
    sents = sent_tokenize(text)
    sents = '. '.join([s.strip().replace("\n", "") for s in sents])
    words = [word for word in sents.lower().split()
             if word not in STOPWORDS and word.isalnum() and word not in stopwords]
    wordnet_lemmatizer = WordNetLemmatizer()
    words = [wordnet_lemmatizer.lemmatize(i) for i in words]
    p_stemmer = PorterStemmer()
    words = [p_stemmer.stem(i) for i in words]
    return words


def get_corpus(text):
    a_list = [process_article(text)]
    dictionary = corpora.Dictionary(a_list)
    return [dictionary.doc2bow(a) for a in a_list]


def get_lda(a_dict, num_topics, num_passes):
    texts = [i[2] for i in a_dict.values()]
    texts = [process_article(a) for a in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    lda = LdaModel(corpus,  # list of lists containing tuples (word index, word freq)
                   id2word=dictionary,  # change nums back to words
                   num_topics=num_topics,  # need to set num topics
                   passes=num_passes)
    return lda
 

def print_lda(lda, num_words=8):
    pp = pprint.PrettyPrinter(indent=4)
    # create prettyprint obj, 8 words for each topic
    pp.pprint(lda.print_topics(num_words=8))


def get_topic(new_article):
    from operator import itemgetter
    new_a = get_corpus(new_article)
#     lda.get_document_topics(new_a[0],minimum_probability=0.05,per_word_topics=False)
    return sorted(lda.get_document_topics(new_a[0],
                                          minimum_probability=0, per_word_topics=False), key=itemgetter(1), reverse=True)


# get news
x = get_cnn('fb')

# print lda model
lda = get_lda(x, 2, 10)
print_lda(lda)

# get topic for single document
a = "'A version of this article first appeared in the Reliable Sources newsletter. You can sign up for free right here.   This is an incredibly difficult time for Alex Trebek, his family members, and the extended Jeopardy! family that spans the globe. Trebek showed tremendous courage by recording a candid video message to fans about his stage 4 pancreatic cancer diagnosis. He even managed to work in a joke about being under contract for three more years. Trebek was diagnosed earlier this week, and his video was released on Wednesday afternoon.  In a time that is all about what is keeping us apart, we got tough news today about someone who has always brought America together, literally for decades, CNN\'s Chris Cuomo said Wednesday night. I don\'t care what your race, color, creed, gender, or bank account level, you\'ve watched Jeopardy. Since 1984 Alex Trebek has been the smartest guy in our living rooms, teaching us, but more importantly, bringing us together. Trebek\'s show puts facts first, Cuomo said, and we need him, now mo"
print(get_topic(a))
