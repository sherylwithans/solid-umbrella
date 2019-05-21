#!pip install webdriver-manager
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
from news_analytics.file_operations import *

def get_cnbc(ticker,num_days):
    url = "https://www.cnbc.com/quotes/?symbol="+ticker +"&tab=news"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    # browser = webdriver.PhantomJS() #replace with .Firefox(), or with the browser of your choice
    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    results_page = BeautifulSoup(innerHTML,'html.parser')

    news_headlines = results_page.find_all('div',class_="assets")
    for item in news_headlines:
        try:
            link = item.find('a').get('href')
        except:
            link = '{{asset.href}}'
        if link != '{{asset.href}}':
            try:
                time,headline,content = get_each_news(link)
                #print('time:',time,'headline:',headline,content)
            except:
                continue
            if time != '--':
                if 'ago' in time.lower():
                    timestring = time
                    pattern =  re.compile(r'\d+')
                    match = re.search(pattern, timestring)
                    if match:
                        if 'mins' in time:
                            datetime_ = datetime.now()-timedelta(minutes=int(match.group()))
                        else:
                            datetime_ = datetime.now()-timedelta(hours=int(match.group()))
                else:    
                    timestring = time
                    pattern =  re.compile(r'[0-9]* [a-zA-Z ]+ [0-9]{4}$')
                    match = re.search(pattern, timestring)
                    if match != None:
                        d = datetime.strptime(match.group(),'%d %B %Y').date()
                        pattern_time = re.compile(r'[0-9]+:[0-9 ]+[A-Z]{2}')
                        match_time = re.search(pattern_time,timestring)
                        #print(datetime.datetime.strptime(match_time.group(),'%I:%M  %p').time())
                        t= datetime.strptime(match_time.group(),'%I:%M  %p').time()
                        datetime_ = datetime.combine(d,t)
                    else:
                        pass
            else:
                datetime_ = time
            #print(type(datetime_),link,datetime_)
            try:
                if datetime_ >= (datetime.now()- timedelta(days=num_days)):
                #news_output_dict[(datetime_,ticker)] = [headline,link,content]
                    write_f("CNBC",ticker,headline,link,datetime_,content)
            except:
                pass


# In[50]:


def get_each_news(headline_link):
    import requests
    from bs4 import BeautifulSoup 
    page = requests.get(headline_link)
    soup = BeautifulSoup(page.content,'lxml')
    
    try:
        headline = soup.find('h1',class_='ArticleHeader-headline').get_text()
    except:
        headline = '--'
    
    try:
        content = soup.find('div',class_='ArticleBody-articleBody').get_text()
        content = content.strip()
    except:
        content = '--'
    
    try:
        #time = soup.find('time',class_='datestamp').get_text()
        time = soup.find('time').get_text()
        time = time.strip()
    except:
        time = '--'
    return time,headline,content

