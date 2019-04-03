#!/usr/bin/env python
# coding: utf-8

# !pip install selenium

def get_selenium_html(url):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    
    browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    results_page = BeautifulSoup(innerHTML,'html')
    return results_page

def get_bs4_html(url):
    from bs4 import BeautifulSoup
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return BeautifulSoup(response.content,"lxml")
        except:
            return "please check for typos"
    
def get_cnn(ticker):
    import re
    from datetime import datetime,timedelta
    
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
    
    def get_info(results_list,n):    
        d={}
        for i in results_list:
            href = 'https:'+i.find('a').get('href') 
            pub_date = get_datetime(href)
            if pub_date and pub_date<=(datetime.now()-timedelta(days=30)):
                return (d,1)
            headline = i.find(class_="cnn-search__result-headline").text.strip()    
            body = i.find(class_="cnn-search__result-body").text.strip()
            d[(pub_date,ticker)]=(headline,href,body)
            n+=1
        return (d,0)
    
    #get AAPL news
    url1 = "https://www.cnn.com/search/?q="+ticker
    results_page1 = get_selenium_html(url1)
    
    p=r' \d+ '
    count = results_page1.find('div',class_='cnn-search__results-count').text
    count = int(re.search(p,count).group().strip())
    
    #get apple news
    url2 = "https://money.cnn.com/quote/news/news.html?symb="+ticker
    results_page2 = get_bs4_html(url2)
    

    d={}
    
    for i in range(count//100+bool(count%100)):
        url = 'https://www.cnn.com/search/?q='+ticker+'&size=100&from='+str(i*100)
        results_list = get_selenium_html(url).find_all('div',class_='cnn-search__result-contents')
        info_dict = get_info(results_list,i*100)
        d.update(info_dict[0])
        if info_dict[1]==1:
            return d       
    return d
