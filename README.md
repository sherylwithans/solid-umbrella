# News Analytics App

The News Analytics App is an interactive platform that will help asset managers gain a high level overview of financial news information.

An automated assistant will allow the asset manager to keep up with the rapid pace of information and news readily available online, so that the manager can focus on his clients. This app will allow asset managers to efficiently and effectively understand the breadth of relevant news articles regarding their client¡¯s portfolios.

The application allows users to:
- View three sentence summaries of financial news articles 
- View sentiment scores of articles
- Visualize top n topics from recent n days news
- Interact with topic visualization bubble plot
- Observe topic importance through relevant topic circle sizes
- Filter database for topic-relevant articles and word tags


## Data
Our news data are scraped from mainstream media,  CNN, CNBC, Reuters and SeekingAlpha. Based on the portfolio position, news related to each stock ticker within user-specified time range are collected and saved in a local SQL database for subsequent sentiment analysis and topic analysis. Users can choose to update the data with current news articles.


## Installation

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all packages from requirements.txt in the folder.

```bash
pip install -r requirements.txt
```
2. Add chromedriver file location to path (to enable web scraping using selenium)

3. Ensure the portfolio data is in a csv file named ¡°portfolio.csv¡± under the directory ¡°News Analytics App/news_analytics/portfolio¡±, with the format below:
- A header row
- First column: Asset name; Second column: Ticker Symbol

## Initialization
- cd to the directory where the app is located

- Run the following command in the shell to initialize the database.
```bash
python setup.py
```

## Load News
- cd to the directory where the app is located

- Run the following command to download recent news within the preset time range. (This process may take a few minutes, and time range can be altered in the file load_news.py)
```bash
python load_news.py
```

## Usage
- cd to the directory where the app is located, and run the following command in the shell.
```bash
python run.py
```
(For subsequent log-in's the user can directly execute run.py)

## Updating News and Database Access
- For updating the news, the user needs to repeat the load news step. 
- If the user wishes to remove rows in the database where web scraping content is null or invalid, they may run
```bash
python db_updates.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
