import os
from dotenv import load_dotenv
import requests


load_dotenv()
api = os.environ.get('api')
url = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey={api}"
response = requests.get(url)
print(response.text)
data1=response.json()
articles = data1.get('articles')
titles=[]
urlimage=[]
urlsite=[]
for i in articles:
    titles.append(i['title'])
    urlimage.append(i['urlToImage'])
    urlsite.append(i['url'])


