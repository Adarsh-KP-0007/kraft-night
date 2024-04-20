from newsapi import NewsApiClient
#import datetime as dt
#import pandas as pd

newsapi = NewsApiClient(api_key='a89fbfe1bfca4f899f939e0d257e6efd')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                            
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2024-04-17',
                                      to='2024-04-18',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)
sources = newsapi.get_sources()
print(top_headlines)
print(all_articles)
print(sources)


