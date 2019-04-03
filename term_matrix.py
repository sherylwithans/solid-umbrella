
# coding: utf-8

# In[ ]:


import nltk
from nltk import sent_tokenize,word_tokenize 
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import pprint #prettyprint

sw = ['aapl','apple']

def process_article(text,stopwords=sw):
    sents = sent_tokenize(text)
    sents = '. '.join([s.strip().replace("\n","") for s in sents])
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

def get_lda(a_dict,num_topics,num_passes):
    texts = [a_dict[key][2] for key in a_dict.keys()]
    texts = [process_article(a) for a in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    lda = LdaModel(corpus,               #list of lists containing tuples (word index, word freq)
                  id2word=dictionary,    #change nums back to words
                  num_topics=num_topics, #need to set num topics
                  passes=num_passes)
    return lda

def print_lda(lda):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lda.print_topics(num_words=8)) #create prettyprint obj, 8 words for each topic

def get_topic(new_article):
    from operator import itemgetter
    new_a = get_corpus(new_article)
#     lda.get_document_topics(new_a[0],minimum_probability=0.05,per_word_topics=False)
    return sorted(lda.get_document_topics(new_a[0],
                    minimum_probability=0,per_word_topics=False),key=itemgetter(1),reverse=True)

def document_term_matrix(a_dict,num_topics,type= 'document_topics'):
    texts = [a_dict[key][2] for key in a_dict.keys()]
    texts = [process_article(a) for a in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(a) for a in texts]
    if type == 'document_topics':
        dt = []
        for i in a_dict:
            dt.append(get_topic(a_dict[i][2]))
        return dt
    if type == 'topic_terms':
        tt = []
        for k,v in dictionary.items():
            pass
        word_map = dictionary.id2token
        for i in range(num_topics):
            tt.append(list(map(lambda x: (word_map[x[0]],x[1]),lda.get_topic_terms(i))))
        return tt
    
def add_topic_info(a_dict):
    result = a_dict
    for key in a_dict.keys():
        if len(a_dict[key]) <= 3:
            content = a_dict[key][2]
            topic = get_topic(content)[0][0]
            result[key].append(topic)
    return result

def document_from_topic(select_topic,a_dict):
    a_dict2 = add_topic_info(a_dict)
    result = []
    for key in a_dict2.keys():
        if a_dict2[key][3] == select_topic:
            result.append(a_dict2[key][1])
    return result

def add_word_info(a_dict):
    result = add_topic_info(a_dict)
    for key in a_dict.keys():
        if len(a_dict[key]) <= 4:
            words = process_article(a_dict[key][2])
            result[key].append(words)
    return result

def document_from_word(word_in,a_dict):
    a_dict2 = add_word_info(a_dict)
    result = []
    word_tag = process_article(word_in)
    if len(word_tag) != 0:
        word_tag = word_tag[0]
        for key in a_dict2.keys():
            words = a_dict2[key][4]
            if word_tag in words:
                result.append(a_dict2[key][1])
    return result

