import requests
  
#Oauth authentication with user credentials
username = "211025@tkmce.ac.in"
password = "abcd1234"
  
#Pre-populated with Production App-Id
App_ID = "bef245bb"
  
#Requesting a bearer token from oauth endpoint
#Review the docs for detailed authentication workflows docs.aylien.com/newsapi/v6
token = requests.post("https://api.aylien.com/v1/oauth/token", auth=(username, password), data={"grant_type": "password"}).json()["access_token"]
  
#Passing the token as a header with App Id
headers = {"Authorization": "Bearer {}".format(token), "AppId":"bef245bb"}
  
#V6 URL
url ='https://api.aylien.com/v6/news/stories?aql=language:(en) AND categories:({{taxonomy:aylien AND id:ay.fin}} OR {{taxonomy:aylien AND id:ay.econ}} OR {{taxonomy:aylien AND id:ay.haw}}) AND sentiment.title.polarity:(negative neutral positive)&cursor=*&published_at.end=NOW&published_at.start=NOW-7DAYS/DAY'

response = requests.get(url, headers=headers)
data = response.json()
data = data.get('stories')



from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from heapq import nlargest

articles_text=[]
for i in range(10):
    articles_text.append(data[i]['body'])

preprocessed_text = []

for article_text in articles_text:
    # Tokenize sentences
    sentences = sent_tokenize(article_text)
    
    # Tokenize words, remove stopwords, and stem words
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [ps.stem(word) for word in words if word.isalnum()]
        for word in words:
            if word not in stop_words:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    # Calculate weighted frequencies
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    # Select top N sentences for summary
    summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    preprocessed_text.append(summary)

#print(preprocessed_text)
# Display summaries
for i, summary in enumerate(preprocessed_text):
    print(f"Summary for article {i + 1}:")
    print(summary)
    print()