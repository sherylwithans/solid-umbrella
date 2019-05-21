from datetime import datetime
from news_analytics.models import Post
from news_analytics import db
from news_analytics.topic_analysis import *
from news_analytics.sentiment_analysis import *

import gensim.summarization
import re


def write_f(news_source, ticker, title, href, date_posted, content):
    print(date_posted)
    if date_posted:
        print(date_posted)
        post_exists = Post.query.filter(
            Post.title.like(title[:15]+'%'),
            Post.ticker.like(ticker),
            Post.date_posted.like(datetime.strftime(date_posted,"%Y-%m-%d")+'%')).first()
        if not post_exists:
            nouns = pick_nouns(content,distinct=True)
            summary = summarize_content(content)
            pos,neg = emotion_analysis(content)
            db.session.add(Post(news_source= news_source,ticker = ticker,title = title, 
                href = href, date_posted=date_posted,content=content,summary=summary,
                pos = pos, neg = neg, nouns = nouns))
            db.session.commit()

p1 = re.compile(r"(?<=\w)(\.)(?=\D)")
p2 = re.compile(r"\w*@")
p3 = re.compile(r"\([^\.]*\)[^ ]*")
p4 = re.compile(r"VIDEO[\d:]*")
p5 = re.compile(r"getElements.*X")
def summarize_content(text):
    striptext = text.replace('\n\n', ' ')
    striptext = striptext.replace('\n', ' ')
    striptext = striptext.replace('U.S.','US')
    striptext = re.sub(p1,r'. ',striptext)
    striptext = re.sub(p2,r'',striptext)
    striptext = re.sub(p3,r'',striptext)
    striptext = re.sub(p4,r'',striptext)
    striptext = re.sub(p5,r'',striptext)
    
    try:
        summary = gensim.summarization.summarize(striptext, word_count=100) 
    except:
        summary = text
    if not summary:
        summary = text
    return summary
