
# coding: utf-8

# In[1]:


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


# In[25]:


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
                                        write_f(str(time),save_dir,content,f"{time},{title},{link}")
                                    else:
                                        return None
    return None


# In[21]:


def get_news_info(url):
    import requests
    import datetime
#     from selenium import webdriver
#     import time
    from bs4 import BeautifulSoup
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(options=options) 
    pre_url = 'https://seekingalpha.com'
    link = pre_url+url
#     driver.get(link)
#    # time.sleep(2)
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


# In[5]:


import pandas as pd
data = pd.read_csv("Common Stock Sample.csv")
data = data.dropna()


# In[ ]:


# all_news_info('fb',3,datetime.datetime.now())


# In[6]:


# new_data = data.iloc[:,:2]


# In[7]:


#tickers = list(new_data['Ticker Symbol'])
#names = list(new_data['Asset Short Name'])


# In[8]:


# def get_names(ticker):
#     pre = 'https://seekingalpha.com/symbol/'
#     url = pre+ticker.upper()
#     from bs4 import BeautifulSoup
#     import requests
   
#     response = requests.get(url)
#     results = BeautifulSoup(response.content,'lxml')
#     name = results.find("div",class_='ticker-title')
#     if name:
#         name = name.get_text().split("|")[0]
#     else:
#         name = get_names2(ticker)
#     return name

# def get_names2(ticker):
#     pre = 'https://seekingalpha.com/symbol/'
#     url = pre+ticker.upper()
#     from bs4 import BeautifulSoup
#     import requests
    
#     from selenium import webdriver
#     import time
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(options=options) 
#     driver.get(url)
#     time.sleep(0.01)
#     response=driver.page_source
    
#    # response = requests.get(url)
#     results = BeautifulSoup(response,'lxml')
#     name = results.find("div",class_='ticker-title')
#     if name:
#         name = name.get_text().split("|")[0]
#     else:
#         name = "* "
#     return name

