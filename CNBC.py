
# coding: utf-8

# In[ ]:


def cnbc_news(ticker):
    news_output_dict = dict()
    url = "https://www.cnbc.com/quotes/?symbol="+ticker +"&tab=news"

    import requests
    from bs4 import BeautifulSoup
    import datetime
    import re
    
    try:
        response = requests.get(url)   
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            try:
                soup = BeautifulSoup(response.content,'lxml')
            except:
                print('something went wrong')
    except:
        print("Something went wrong with request.get")
    
    news_headlines = soup.find_all('div',class_="assets")
    for item in news_headlines:
        link = item.find('a').get('href')
        if link != '{{asset.href}}':
            time,headline,content = get_each_news(link)
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
           
            news_output_dict[(datetime_,ticker)] = [headline,link,content]
    
    return news_output_dict


# In[ ]:


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

