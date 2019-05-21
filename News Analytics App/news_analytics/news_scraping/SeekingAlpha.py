from news_analytics.file_operations import *
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import datetime


def get_sa_html(ticker):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options) 
    driver.get('https://seekingalpha.com/symbol/'+ticker)
    time.sleep(3)
    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
    execute_times(5)
    time.sleep(3)
    html=driver.page_source
    return html



def get_seekingalpha(ticker,days=3,date=datetime.datetime.now()):
    ticker = ticker.upper()
    save_dir = "news/"+ticker+"/SeekingAlpha"
    html = get_sa_html(ticker)
    from bs4 import BeautifulSoup
    results = BeautifulSoup(html,'lxml')
    b = results.find('div',{'column':'news','data-page-title':'Analysis & News'})
    if b:
        a = b.find_all('li',class_='symbol_item')
        time_range = recent_n_days(date,days)
        for i in a:
            if i :
                if i.find('div',class_='content'):
                    if i.find('div',class_='content').find('div',class_='symbol_article'):
                        if i.find('div',class_='content').find('div',class_='symbol_article').find('a'):
                            url = i.find('div',class_='content').find('div',class_='symbol_article').find('a').get('href')
                            title = i.find('div',class_='content').find('div',class_='symbol_article').find('a').get_text()
                            #print(url)
                            if url:
                                if url.split('/')[1] != 'news':
                                    continue
                                time,link,content = get_news_info(url)
                                #print(time)
                                if time:
                                    if time >= time_range[-1]:
                                      #  print(time)
                                        content = content.strip()
                                        write_f('Seeking Alpha',ticker,title,link,time,content)
                                    else:
                                        return None
    return None


# In[21]:


def get_news_info(url):
    import requests
    import datetime
    from bs4 import BeautifulSoup
    pre_url = 'https://seekingalpha.com'
    link = pre_url+url
    response=requests.get(link)
    response2 = BeautifulSoup(response.content,'lxml')
    if response2.find('time'):
        time_ = response2.find('time').get('datetime')[:19]
        time_ = datetime.datetime.strptime(time_,'%Y-%m-%d %H:%M:%S')
    elif response2.find('div',class_='filing-info'):
        t = response2.find('div',class_='filing-info').find('span').get_text()
        def parse_t(t):
            t = t[:22]
            if t[5] == ' ':
                t = t[:5]+'0'+t[6:]
            if t[14] == ' ':
                t = t[:14]+'0'+t[15:]
            return t
        t = parse_t(t)
        time_ = datetime.datetime.strptime(t,'%b. %d, %Y %I:%M %p')
    if response2.find('div',{'id':'bullets_ul'}):
        c = response2.find('div',{'id':'bullets_ul'}).find_all('p')
        content = ''
        for i in c:
            content += i.get_text()
        return time_,link,content
    return None,None,None


# In[4]:


def recent_n_days(date,n):
    date_list = []
    for i in range(0,n):
        day = date-datetime.timedelta(days=i)
        day = datetime.datetime.strptime(str(day.date())+'000000','%Y-%m-%d%H%M%S')
        date_list.append(day)
    return date_list

