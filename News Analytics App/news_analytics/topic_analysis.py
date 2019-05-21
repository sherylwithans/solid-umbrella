import numpy as np
from operator import itemgetter

# install nltk, selenium, genism and bs4, pyLDAvis
# install chromedriver and add to path

# ntlk imports
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# prettyprint
import pprint

# genism imports
from gensim import corpora,models
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

from datetime import datetime, timedelta
import pyLDAvis.gensim

import re

user_stopwords = ['zacks']  # user defined stopwords


#https://radimrehurek.com/gensim/models/tfidfmodel.html
# models.TfidfModel: normalize=True by default,normalize document vectors to unit euclidean length.You can also inject your own function into normalize.
#slope=0.65 by default: Parameter required by pivoted document length normalization which determines the slope to which the old normalization can be tilted. This parameter only works when pivot is defined.
def tf_idf(corpus):
    average_count=[]
    for item in corpus:
        if len(item) != 0:
            average_count.append(np.mean(item,axis=0)[1])
        else:
            average_count.append(0)
    pivot = np.mean(average_count)    
    tfidf = models.TfidfModel(corpus,pivot=pivot)
    corpus_tfidf = tfidf[corpus]
    return corpus_tfidf


def print_lda(lda, num_words=8):
# prints lda model coefficients, user can specify number of words to include for each topic
    pp = pprint.PrettyPrinter(indent=4)
    # create prettyprint obj, 8 words for each topic
    pp.pprint(lda.print_topics(num_words=8))


def get_topic(article_number,lda,corpus_tfidf):
# for a single article (text string), given the order of the article on the loaded news list, returns list of relevant topics ordered by likelihood
    #single_corpus = get_corpus(article) 
#     lda.get_document_topics(new_a[0],minimum_probability=0.05,per_word_topics=False)
    return sorted(lda.get_document_topics(corpus_tfidf[article_number],minimum_probability=0, per_word_topics=False),
                  key=itemgetter(1), reverse=True)


def get_lda_noun(news_list, num_topics, num_passes,cache='cache',stopwords=user_stopwords):
# input: list of noun articles ([date,text string] list), number of topics (int), number of passes (int)
# output: lda model and corpus_tfidf
    texts = [process_article_noun(pick_nouns(a[1])) for a in news_list]
    texts = [a for a in texts if a]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    corpus_tfidf = tf_idf(corpus)
    lda = LdaModel(corpus_tfidf,  # list of lists containing tuples (word index, word freq)
                   id2word=dictionary,  # change nums back to words
                   num_topics=num_topics,  # need to set num topics
                   passes=num_passes)
    lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_display, './news_analytics/lda/lda_'+cache+'.html')
    return lda,corpus_tfidf

p1 = re.compile(r"(?<=\w)(\.)(?=\D)")
p2 = re.compile(r"\w*@")
p3 = re.compile(r"\([^\.]*\)[^ ]*")
p4 = re.compile(r"VIDEO[\d:]*")
p5 = re.compile(r"getElements.*X")
def process_article_noun(text,stopwords=user_stopwords):
# for single article (text string), tokenize and lemmatize data, return list of word stems
# for topic analysis on nouns
    striptext = text.replace('U.S.','US')
    striptext = re.sub(p1,r'. ',striptext)
    striptext = re.sub(p2,r'',striptext)
    striptext = re.sub(p3,r'',striptext)
    striptext = re.sub(p4,r'',striptext)
    striptext = re.sub(p5,r'',striptext)
    sents = sent_tokenize(text)
    sents = '. '.join([s.strip().replace("\n", "") for s in sents])
    words = [word for word in sents.lower().split()
             if word not in STOPWORDS and word.isalnum() and word not in stopwords]
    wordnet_lemmatizer = WordNetLemmatizer()
    words = [wordnet_lemmatizer.lemmatize(i) for i in words]
    words = [word for word in words if len(word)>3]
    return words

def pick_nouns(doc,stopwords=user_stopwords,distinct=False):
# input: doc (str) and stopwords (list)
# output: list of nouns (list)
    import nltk
    stopwords = [x.upper() for x in stopwords]
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sens = sent_detector.tokenize(doc)
    wpos = []
    for i in sens:
        word_list = nltk.word_tokenize(i)
        wpos.extend(nltk.pos_tag(word_list))
    result = []
    for i in wpos:
        if i[1] == 'NNP':
            word = i[0]
            if word.upper() not in stopwords and word.isalpha() :
                result.append(i[0])
    if distinct:
        result = list(set(result))
    return ' '.join(result)