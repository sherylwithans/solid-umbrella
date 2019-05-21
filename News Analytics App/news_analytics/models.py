from datetime import datetime
from news_analytics import db 

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    news_source = db.Column(db.String(100),nullable=False)
    ticker = db.Column(db.String(20),nullable=False)
    title= db.Column(db.String(100), nullable = False)
    href= db.Column(db.String(300),nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    pos = db.Column(db.String(10), nullable=False)
    neg = db.Column(db.String(10), nullable=False)
    nouns = db.Column(db.Text,nullable=True)
    topic_id = db.Column(db.Integer,nullable=True)


    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"





