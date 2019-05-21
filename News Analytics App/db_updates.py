from news_analytics.models import Post
from news_analytics import db

from news_analytics.file_operations import *
import gensim.summarization
import re

posts = Post.query.all()

for post in posts:
    # update summaryin db
    post.summary = summarize_content(post.content)
    db.session.commit()



# for post in posts:
#     # if content is null, remove from db
#     if sum([w.isalnum() for w in post.content.split(' ')]) == 0:
#         db.session.delete(post)
#         db.session.commit()
