import json
import requests

page = requests.get('https://timesofindia.indiatimes.com/nri/us-canada-news/more-h-1b-visa-holders-are-switching-jobs-the-process-explained/articleshow/109460294.cms')

res = json.load(page)
print(res)

