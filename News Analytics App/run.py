# pip install flask, flask-wtf, flask-sqlalchemy, flask-bcrpt
# pip install flask-login

from news_analytics import app

# from news_analytics.news_scraping import CNN
# from news_analytics.news_scraping import Reuters
# from news_analytics.news_scraping import SeekingAlpha

if __name__=='__main__':
    # only true if run script directly, else name = module name
    app.run(debug=False)
