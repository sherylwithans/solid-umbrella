import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from news_analytics.file_operations import *

def find_link(news):
    result = []
    news_pre = 'https://www.reuters.com'
    for i in news:
        link = i.find('a').get('href')
        title = i.find('a').get_text()
        if title:
            link = news_pre+link
            result.append((title,link))
    return result

def get_content(link):
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    para = results.find_all('p')
    content = ''
    for i in para[1:-3]:
        content = content+i.get_text()
    return content

def recent_10_news(ticker):
    pre_url = 'https://www.reuters.com/finance/stocks/company-news/'
    url = pre_url+ticker
    response = requests.get(url)
    results = BeautifulSoup(response.content,'lxml')
    news = results.find_all('h2')
    links = find_link(news)
    content = []
    for link in links:
        content.append(get_content(link[1])) 
    return content

def get_info(link):
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    time = results.find('div',{'class':'ArticleHeader_date'}).get_text()
    time = [i.strip() for i in time.split('/')]
    time = time[0].split(',')[0].split(' ')[0] + ' ' + "%02d" % int(time[0].split(',')[0].split(' ')[1]) + ' '+            time[0].split(',')[1].strip() + ' ' +             '%02d'%int(time[1].split(':')[0]) + ':' + '%02d'%int(time[1].split(':')[1].split(' ')[0]) + time[1].split(' ')[1]
    time = datetime.strptime(time,'%B %d %Y %I:%M%p')
    para = results.find_all('p')
    content = ''
    for i in para[1:-3]:
        content = content+i.get_text()
    return time,content

def get_title(link):
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    title = results.find('h1',{'class':'ArticleHeader_headline'}).get_text()
    return title

def get_time(link):
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    time = results.find('div',{'class':'ArticleHeader_date'}).get_text()
    time = [i.strip() for i in time.split('/')]
    time = time[0].split(',')[0].split(' ')[0] + ' ' + "%02d" % int(time[0].split(',')[0].split(' ')[1]) + ' '+            time[0].split(',')[1].strip() + ' ' +             '%02d'%int(time[1].split(':')[0]) + ':' + '%02d'%int(time[1].split(':')[1].split(' ')[0]) + time[1].split(' ')[1]
    time = datetime.strptime(time,'%B %d %Y %I:%M%p')
    return time

def get_final_ticker(results,ticker):
    final_ticker = results.find('div',{'id':'sectionTitle'})
    if final_ticker == None:
        return None
    else:
        final_ticker = final_ticker.find('h1').get_text().split('(')[1].split(')')[0]
        if ticker.upper() == final_ticker[:len(ticker)]:
            return final_ticker
        else:
            return None
        
def recent_n_days(date,n):
    date_list = []
    for i in range(0,n):
        day = date-timedelta(days=i)
        day = "%02d" % day.month+"%02d" % day.day+"%04d" % day.year
        date_list.append(day)
    return date_list

def get_reuters(ticker,days=3,date=datetime.now()):
    ticker = ticker.upper()
    pre_url = 'https://www.reuters.com/finance/stocks/company-news/'
    url = pre_url+ticker
    response = requests.get(url)
    results = BeautifulSoup(response.content,'lxml')
    final_ticker = get_final_ticker(results,ticker)
    if final_ticker:
        dates=recent_n_days(date,days)
        for d in dates:
            url=pre_url+final_ticker+'?date='+d
            response = requests.get(url)
            results = BeautifulSoup(response.content,'lxml')
            news = results.find_all('h2') 
            links = find_link(news)
            for link in links: #(datetime,ticker):[title,link,article]
                if link:
                    title=link[0]
                    time,content=get_info(link[1])
                    content = content.strip()
                    write_f('Reuters',ticker,title,link[1],time,content)
