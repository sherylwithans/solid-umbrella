
# coding: utf-8

# In[7]:


import datetime

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
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    para = results.find_all('p')
    content = ''
    for i in para[1:-3]:
        content = content+i.get_text()
    return content

def recent_10_news(ticker):
    import requests
    from bs4 import BeautifulSoup
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

def recent_3days_news(ticker,date=datetime.datetime.now()):
    import requests
    from bs4 import BeautifulSoup
    pre_url = 'https://www.reuters.com/finance/stocks/company-news/'
    url = pre_url+ticker
    response = requests.get(url)
    results = BeautifulSoup(response.content,'lxml')
    final_ticker = get_final_ticker(results,ticker)
    news_dict = dict()
    if final_ticker:
        dates=recent_3_days(date)
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
                    news_dict[(time,ticker)] = [title,link,content]
    return news_dict

def get_info(link):
    from datetime import datetime
    import requests
    from bs4 import BeautifulSoup
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
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(link)
    results = BeautifulSoup(response.content,'lxml')
    title = results.find('h1',{'class':'ArticleHeader_headline'}).get_text()
    return title

def get_time(link):
    import requests
    from bs4 import BeautifulSoup
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
        
def recent_3_days(date):
    import datetime
    now = date
    yes = now - datetime.timedelta(days=1)
    bef_yes = now - datetime.timedelta(days=2)
    now = "%02d" % now.month+"%02d" % now.day+"%04d" % now.year
    yes = "%02d" % yes.month+"%02d" % yes.day+"%04d" % yes.year
    bef_yes = "%02d" % bef_yes.month+"%02d" % bef_yes.day+"%04d" % bef_yes.year
    return bef_yes,yes,now

