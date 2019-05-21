import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash,redirect, request, abort, send_file
from news_analytics import app, db, bcrypt
from news_analytics.forms import PostForm 
from news_analytics.models import Post 
from news_analytics.topic_analysis import *
from news_analytics.sentiment_analysis import *
from news_analytics.file_operations import *

from datetime import datetime
import secrets
import csv

def get_portfolio():
    portfolio = []
    prev = datetime.now()-timedelta(days=7)
    with open('./news_analytics/portfolio/portfolio.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count=0
        for row in csv_reader:
            if line_count !=0:
                if len(row[0])>0:
                    name = row[0]
                    ticker = row[1]
                    posts = db.session.query(Post.content).filter(Post.ticker == ticker,Post.date_posted>=prev).order_by(Post.date_posted.desc()).all()
                    posts = [a[0] for a in posts]
                    neg,pos = exp_smooth(posts)
                    neg = str(neg)[:5]
                    pos = str(pos)[:5]
                    tag = f"{name} ({ticker})"
                    portfolio.append((tag,pos,neg,ticker))
            line_count+=1
    return portfolio

PORTFOLIO = get_portfolio()

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=7)

    return render_template('home.html',posts=posts,portfolio=PORTFOLIO)

@app.route('/home/<string:ticker>')
def ticker_home(ticker):
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter(Post.ticker==ticker).order_by(Post.date_posted.desc()).paginate(page = page, per_page=7)

    return render_template('home.html',posts=posts,portfolio=PORTFOLIO)


@app.route('/topic_analysis/new',methods=['GET','POST'])
def new_topic_analysis():
    form = PostForm()
    if form.validate_on_submit():  
        prev = datetime.now()-timedelta(days=int(form.num_days.data))
        news_list = Post.query.filter(Post.date_posted>=prev).all()
        if news_list == []:
            flash(f"There isn't any news in the time interval you selected. \
                Please enter a larger number of days",'danger')
            return render_template('create_topic_analysis.html',title='Generate Topic Analysis',
                form = form, legend = 'Generate Topic Analysis',portfolio=PORTFOLIO)
        cache = secrets.token_hex(8)
        return redirect(url_for('topic_analysis',num_days=form.num_days.data,num_topics=form.num_topics.data,cache=cache))
    return render_template('create_topic_analysis.html',title='Generate Topic Analysis',
        form = form, legend = 'Generate Topic Analysis',portfolio=PORTFOLIO)

@app.route('/topic_analysis/<int:num_days>/<int:num_topics>/<string:cache>')
def topic_analysis(num_days,num_topics,cache):
    exists = os.path.isfile('./news_analytics/lda/lda_'+cache+'.html')
    posts_noun = []
    if exists:
        prev = datetime.now()-timedelta(days=num_days)
        posts = Post.query.filter(Post.date_posted>=prev).all()

        for post in posts:
            if pick_nouns(post.content):
                posts_noun.append(post)

    else:
        prev = datetime.now()-timedelta(days=num_days)
        news_list = db.session.query(Post.date_posted,Post.content).filter(Post.date_posted>=prev).all()
        lda, corpus_tfidf = get_lda_noun(news_list,num_topics,10,cache)
        posts = Post.query.filter(Post.date_posted>=prev).all()

        i = 0
        for post in posts:
            if pick_nouns(post.content):
                post.topic_id = get_topic(i,lda,corpus_tfidf)[0][0]+1
                db.session.commit()
                posts_noun.append(post)
                i+=1
        flash(f'Your topic analysis visualisation for recent {num_days} days has been generated!','success')
    
    topic_summaries = []
    for i in range(0,num_topics):
        i+=1
        text=''
        for post in posts_noun:
            if post.topic_id == i:
                    text+=' '+post.content
        text =summarize_content(text)
        topic_summaries.append((i,text))
    
    return render_template('topic_analysis.html',title='Topic Analysis', 
        hide_nav = 'True',cache=cache,posts=posts_noun,topic_summaries = topic_summaries)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post = post)

@app.route('/lda/<string:cache>')
def show_lda(cache):

    return send_file('./lda/lda_'+cache+'.html')
