from newsapi import NewsApiClient
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from heapq import nlargest

# Initialize NLTK
import nltk

# Initialize News API client
newsapi = NewsApiClient(api_key='a89fbfe1bfca4f899f939e0d257e6efd')

# Fetch news articles

articles = newsapi.get_everything(q='technology',
                                      from_param='2024-04-17',
                                      to='2024-04-18',
                                      language='en',
                                      sort_by='relevancy',
                                      page_size=20,
                                      page=2)
# Extract and preprocess text from articles
print(articles)
articles_text = [article['content'] for article in articles['articles'] if article['content']]

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

