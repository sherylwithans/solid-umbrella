
# coding: utf-8

# In[ ]:


import numpy as np
from operator import itemgetter
# web scraping imports
from CNN import *
from Reuters import *
from SeekingAlpha import *
from CNBC import *

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
from gensim import corpora,models
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

stopwords = []  # user defined stopwords

def process_article(text):
# for single article (text string), tokenize and lemmatize data, return list of word stems
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
# for single article (text string), tokenize data and return corpus (list of lists)
    a_list = [process_article(text)]
    dictionary = corpora.Dictionary(a_list)
    return [dictionary.doc2bow(a) for a in a_list]


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


def get_lda(news_list, num_topics, num_passes):
# for list of articles ([date,text string] list), generate lda model
    texts = [process_article(a[1]) for a in news_list]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    corpus_tfidf = tf_idf(corpus)
    lda = LdaModel(corpus_tfidf,  # list of lists containing tuples (word index, word freq)
                   id2word=dictionary,  # change nums back to words
                   num_topics=num_topics,  # need to set num topics
                   passes=num_passes)
    return lda,corpus_tfidf
 

def print_lda(lda, num_words=8):
# prints lda model coefficients, user can specify number of words to include for each topic
    pp = pprint.PrettyPrinter(indent=4)
    # create prettyprint obj, 8 words for each topic
    pp.pprint(lda.print_topics(num_words=8))


def get_topic(article_number,corpus_tfidf):
# for a single article (text string), given the order of the article on the loaded news list, returns list of relevant topics ordered by likelihood
    #single_corpus = get_corpus(article) 
#     lda.get_document_topics(new_a[0],minimum_probability=0.05,per_word_topics=False)
    return sorted(lda.get_document_topics(corpus_tfidf[article_number],minimum_probability=0, per_word_topics=False),
                  key=itemgetter(1), reverse=True)


# In[ ]:


def get_lda_noun(nouns_list, num_topics, num_passes):
# input: list of nouns (list), number of topics (int), number of passes (int)
# output: lda model and corpus_tfidf
    texts = [process_article_noun(a) for a in nouns_list]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    corpus_tfidf = tf_idf(corpus)
    lda = LdaModel(corpus_tfidf,  # list of lists containing tuples (word index, word freq)
                   id2word=dictionary,  # change nums back to words
                   num_topics=num_topics,  # need to set num topics
                   passes=num_passes)
    return lda,corpus_tfidf

def process_article_noun(text):
# for single article (text string), tokenize and lemmatize data, return list of word stems
# for topic analysis on nouns
    sents = sent_tokenize(text)
    sents = '. '.join([s.strip().replace("\n", "") for s in sents])
    words = [word for word in sents.lower().split()
             if word not in STOPWORDS and word.isalnum() and word not in stopwords]
    wordnet_lemmatizer = WordNetLemmatizer()
    words = [wordnet_lemmatizer.lemmatize(i) for i in words]
    #p_stemmer = PorterStemmer()
    #words = [p_stemmer.stem(i) for i in words]
    return words

def pick_nouns(doc,stopwords):
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
            if i[0].upper() not in stopwords:
                result.append(i[0])
    return result

def noun_lda(doc_list,stopwords,numTopic,numPass):
# input: list of news (list), stopwords(case does not matter) (list) , number of topics (int) and number of passes (int)
# output: lda model and corpus_tfidf
    nouns = []
    for i in text:
        nouns.append(' '.join(pick_nouns(i,stopwords)))
    lda,corpus_tfidf = get_lda_noun(nouns, numTopic, numPass)
    return lda,corpus_tfidf


# In[ ]:


def load_dict():
# load negative and positive dictionaries
    import os
    def get_dict_words(dict_dir):
        with open(dict_dir,'r') as f:
            words = []
            for line in f:
                words.append(line.replace('\n','').lower())
        return words
    
    neg = get_dict_words(os.getcwd() + '\\dictionaries\\negative.txt')
    pos = get_dict_words(os.getcwd() + '\\dictionaries\\positive.txt')
    return neg,pos

def emotion_analysis(text):
# input: text (string)
# output: negative and positive score
    neg,pos = load_dict()
    from nltk import word_tokenize
    results = dict()
    c1 = c2 = 0
    for word in word_tokenize(text):
        word = word.lower()
        if word in neg:
            c1 += 1
        if word in pos:
            c2 += 1
    n = len(word_tokenize(text))
    results['negative'] = c1/n
    results['positive'] = c2/n
    return results

def emotion_analyzer(text_list):
# input: list of texts (list)
# output: dataframe containing negative and positive scores of each text
    import pandas as pd
    df = pd.DataFrame(columns=['negative','positive'])
    count = 1
    for text in text_list:
        a = emotion_analysis(text[1])
        df.loc[count] = [a['negative'],a['positive']]
        count += 1
    return df


# In[ ]:


def sort_text(news):
#turn news into a list of text, ordered from the newest to the latest
#input: news: list of (datetime,news) from load_news()
    sorted_news = sorted(news, key=lambda article: article[0],reverse=True)
    texts_list = list(map(itemgetter(1),sorted_news))
    return texts_list
    

def document_term_matrix(texts_list,num_topics,lda,stopwords,type= 'topic_terms'):
# input: list of texts (list), number of topics (int), lda model, list of stopwords (list), type of matrix generated (string)
# output: matrix (list)
    texts = [process_article_noun(a) for a in texts_list]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    
    nouns = []
    for i in texts_list:
        nouns.append(' '.join(pick_nouns(i,stopwords)))
    texts = [process_article_noun(a) for a in nouns]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    corpus_tfidf = tf_idf(corpus)
    
    if type == 'document_topics':
        dt = []
        for i in range(len(texts_list)):
            dt.append(get_topic(i,corpus_tfidf))
        return dt
    if type == 'topic_terms':
        tt = []
        for k,v in dictionary.items():
            pass
        word_map = dictionary.id2token
        for i in range(num_topics):
            tt.append(list(map(lambda x: (word_map[x[0]],x[1]),lda.get_topic_terms(i))))
        return tt
    
def exp_smooth(alpha,text_list):
# input: alpha in the exponential smoothing equation (double), list of texts (list)
# output: conslidated sentimental scores (tuple of doubles)
    neg = []
    pos = []
    for d in text:
        neg.append(emotion_analysis(d)['negative'])
        pos.append(emotion_analysis(d)['positive'])
    for i in range(len(text)):
        if i == 0:
            neg_s = neg[len(pos)-i-1]
            pos_s = pos[len(pos)-i-1]
        else:
            neg_s = alpha*neg[len(pos)-i-1] + (1-alpha)*neg_s
            pos_s = alpha*pos[len(pos)-i-1] + (1-alpha)*pos_s
    return neg_s,pos_s

