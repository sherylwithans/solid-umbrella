
# coding: utf-8

# In[92]:


from file_operations import *
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import datetime
def get_sa_html(ticker):
    from selenium import webdriver
    import time
    from bs4 import BeautifulSoup
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options) 
    driver.get('https://seekingalpha.com/symbol/'+ticker)
    time.sleep(3)
    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
    execute_times(5)
    time.sleep(5)
    html=driver.page_source
    return html


# In[93]:


def all_news_info(ticker,days=3,date=datetime.datetime.now()):
    ticker = ticker.upper()
    save_dir = "news/"+ticker+"/SeekingAlpha"
    make_dir(save_dir)
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
                            time,link,content = get_news_info(url)
                            if time:
                                if (time >= time_range[-1]) & (time <= time_range[0]):
                                    content = content.strip()
                                    write_f(str(time),save_dir,content,f"{time},{title},{link[1]}")
                                else:
                                    return None
    return None


# In[94]:


def get_news_info(url):
    import requests
    import datetime
    from selenium import webdriver
    import time
    from bs4 import BeautifulSoup
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options) 
    pre_url = 'https://seekingalpha.com'
    link = pre_url+url
    driver.get(link)
    time.sleep(5)
    response=driver.page_source
    response2 = BeautifulSoup(response,'lxml')
    if response2.find('time'):
        time = response2.find('time').get('datetime')[:19]
        time = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        c = response2.find('div',{'id':'bullets_ul'}).find_all('p')
        content = ''
        for i in c:
            content += i.get_text()
        return time,link,content
    return None,None,None


# In[95]:


def recent_n_days(date,n):
    date_list = []
    for i in range(0,n):
        day = date-datetime.timedelta(days=i)
        day = datetime.datetime.strptime(str(day.date())+'000000','%Y-%m-%d%H%M%S')
        date_list.append(day)
    return date_list


# In[97]:


# all_news_info('fb',days=5,date=datetime.datetime.now())

