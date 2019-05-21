from selenium import webdriver
from bs4 import BeautifulSoup

import requests
import re
from datetime import datetime,timedelta

from news_analytics.file_operations import *


def get_selenium_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    # browser = webdriver.PhantomJS() #replace with .Firefox(), or with the browser of your choice
    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    results_page = BeautifulSoup(innerHTML,'html.parser')
    return results_page

def get_bs4_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return BeautifulSoup(response.content,"lxml")
        except:
            print("please check for typos")

def get_datetime(url):
    try:
        dates = get_bs4_html(url).find('p',class_='update-time').text.strip().split(",")
        p_time=r'[\d: APM]+'
        time = re.search(p_time,dates[0])
        date = dates[1].strip().split(' ')[1:]
        date.append(dates[2].strip())
        date = ' '.join(date+[time.group().strip()])
        return datetime.strptime(date,'%B %d %Y %I:%M %p')
    except:
        return None

def search_by_ticker(ticker,num_days,search_interval): 
    url = "https://www.cnn.com/search/?q="+ticker
    results_page = get_selenium_html(url)
    if not results_page:
        return
    
    p=r' \d+ '
    count = results_page.find('div',class_='cnn-search__results-count').text
    if not count:
        return
    count = int(re.search(p,count).group().strip())

    for i in range(count//search_interval+bool(count%search_interval)):
        url = 'https://www.cnn.com/search/?q='+ticker+'&size=20&from='+str(i*search_interval)
        results_list = get_selenium_html(url).find_all('div',class_='cnn-search__result-contents')
        for i in results_list:
            href = 'https:'+i.find('a').get('href') 
            pub_date = get_datetime(href)
            if pub_date and pub_date<=(datetime.now()-timedelta(days=num_days)):
                return
            headline = i.find(class_="cnn-search__result-headline").text.strip()    
            body = i.find(class_="cnn-search__result-body").text.strip()
            # pos,neg = emotion_analysis(body)
            write_f('CNN',ticker,headline,href,pub_date,body)

def search_by_company(ticker,num_days):
    url = "https://money.cnn.com/quote/news/news.html?symb="+ticker
    results_page = get_bs4_html(url)
    if not results_page:
        return
    table = results_page.find('table',class_='wsod_newsTable')
    try:
        a_tags = [rd.get('href') for r in table.find_all('tr') for rd in r.find_all('a')]
    except:
        return
    for i in range(len(a_tags)):
        href = a_tags[i]
        if href[:20]=="http://www.zacks.com":
            href = "https"+href[4:]
            result_page = get_selenium_html(href)
            if result_page.find("article") and result_page.find("article").find("time"):
                pub_date = datetime.strptime(result_page.find("article").find("time").text,'%B %d, %Y')
            else:
                return
            if pub_date and pub_date<=(datetime.now()-timedelta(days=num_days)):
                continue
            headline = result_page.find("article").find("h1").text
            body = result_page.find("div",class_="commentary_body")
            if body:
                body = "".join([i.text.strip() for i in body.find_all('p')])
                write_f('CNN',ticker,headline,href,pub_date,body)
        elif href[:20]=="https://www.fool.com":
            result_page = get_bs4_html(href)
            pub_date = result_page.find("div",class_="publication-date").text.strip()
            pub_date = datetime.strptime(pub_date,'%b %d, %Y at %I:%M%p')
            if pub_date and pub_date<=(datetime.now()-timedelta(days=num_days)):
                continue
            headline = result_page.find("h1").text
            body = result_page.find("span",class_="article-content").find_all("p")
            body = "".join([i.text.strip() for i in body])
            write_f('CNN',ticker,headline,href,pub_date,body)


def get_cnn(ticker,days=3,search_interval=20):
    # default search past 3 days, flipping 20 items per page
    
    ticker = ticker.upper()
    
    #search site by ticker
    search_by_ticker(ticker,days,search_interval)

    #search site by company tag
    search_by_company(ticker,days)

