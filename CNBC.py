
# coding: utf-8

# In[1]:


#!pip install webdriver-manager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import datetime
from file_operations import *


# In[16]:


from file_operations import *
def cnbc_news(ticker):
    #news_output_dict = dict()
    url = "https://www.cnbc.com/quotes/?symbol="+ticker +"&tab=news"
    save_dir = "news/"+ticker+"/CNBC"
    make_dir(save_dir)
    
#     try:
#         response = requests.get(url)   
#         if not response.status_code == 200:
#             print("HTTP error",response.status_code)
#         else:
#             try:
#                 soup = BeautifulSoup(response.content,'lxml')
#             except:
#                 print('something went wrong')
#     except:
#         print("Something went wrong with request.get")
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
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
            except:
                pass
            if time != '--':
                if 'Ago' in time:
                    timestring = time
                    pattern =  re.compile(r'\d+')
                    match = re.search(pattern, timestring)
                    if 'mins' in time:
                        datetime_ = datetime.datetime.now()-datetime.timedelta(minutes=int(match.group()))
                    else:
                        datetime_ = datetime.datetime.now()-datetime.timedelta(hours=int(match.group()))
                else:    
                    timestring = time
                    pattern =  re.compile(r'[0-9]* [a-zA-Z ]+ [0-9]{4}$')
                    match = re.search(pattern, timestring)
                    #print(match)
                    d = datetime.datetime.strptime(match.group(),'%d %B %Y').date()
                    pattern_time = re.compile(r'[0-9]+:[0-9 ]+[A-Z]{2}')
                    match_time = re.search(pattern_time,timestring)
                    #print(datetime.datetime.strptime(match_time.group(),'%I:%M  %p').time())
                    t= datetime.datetime.strptime(match_time.group(),'%I:%M  %p').time()
                    datetime_ = datetime.datetime.combine(d,t)
            else:
                datetime_ = time
           
            #news_output_dict[(datetime_,ticker)] = [headline,link,content]
            write_f(str(datetime_),save_dir,content,f"{datetime_},{headline},{link}")


# In[3]:


def get_each_news(headline_link):
    import requests
    from bs4 import BeautifulSoup 
    page = requests.get(headline_link)
    soup = BeautifulSoup(page.content,'lxml')
    
    try:
        headline = soup.find('h1',class_='title').get_text()
    except:
        headline = '--'
    
    try:
        content = soup.find('article').get_text()
        content = content.strip()
    except:
        content = '--'
    
    try:
        time = soup.find('time',class_='datestamp').get_text()
        time = time.strip()
    except:
        time = '--'
    return time,headline,content


# In[17]:


cnbc_news('AAPL')

