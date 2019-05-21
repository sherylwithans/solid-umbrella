import os


def load_dict():
# load negative and positive dictionaries
    def get_dict_words(dict_dir):
        with open(dict_dir,'r') as f:
            words = []
            for line in f:
                words.append(line.replace('\n','').lower())
        return words
    
    neg = get_dict_words(os.getcwd() + '\\news_analytics\\dictionaries\\negative.txt')
    pos = get_dict_words(os.getcwd() + '\\news_analytics\\dictionaries\\positive.txt')
    return neg,pos

def emotion_analysis(text):
# input: text (string)
# output: negative and positive score
    neg,pos = load_dict()
    from nltk import word_tokenize
    # results = dict()
    c1 = c2 = 0
    for word in word_tokenize(text):
        word = word.lower()
        if word in neg:
            c1 += 1
        if word in pos:
            c2 += 1
    if c1+c2 > 0:
        neg = c1/(c1+c2)
        pos = c2/(c1+c2)
    else:
        neg = 0
        pos = 0
    return pos,neg

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
    
def exp_smooth(text_list,alpha=0.6):
# input: list of texts (list, most recent news first),alpha in the exponential smoothing equation (double)
# output: conslidated sentimental scores (tuple of doubles)
    neg = []
    pos = []
    for d in text_list:
        neg.append(emotion_analysis(d)[1])
        pos.append(emotion_analysis(d)[0])
    for i in range(len(text_list)):
        if i == 0:
            neg_s = neg[len(pos)-i-1]
            pos_s = pos[len(pos)-i-1]
        else:
            neg_s = alpha*neg[len(pos)-i-1] + (1-alpha)*neg_s
            pos_s = alpha*pos[len(pos)-i-1] + (1-alpha)*pos_s
    if len(text_list) == 0:
        return 0,0
    return neg_s,pos_s

