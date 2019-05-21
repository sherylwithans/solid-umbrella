from news_analytics.news_scraping.CNN import get_cnn
from news_analytics.news_scraping.Reuters import get_reuters
from news_analytics.news_scraping.SeekingAlpha import get_seekingalpha
from news_analytics.news_scraping.CNBC import get_cnbc

import csv

with open('./news_analytics/portfolio/portfolio.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    days = 5
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'Getting data for {row[0]}: {row[1]}')
            t = row[1]
            get_cnn(t,days)
            get_reuters(t,days)
            get_seekingalpha(t,days)
            get_cnbc(t,days)


