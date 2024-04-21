from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout

from .forms import *
from .models import *

import random
import os
from dotenv import load_dotenv
import requests

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from heapq import nlargest

def home(request):

    fullset=[]
    
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey=a965c9913dd043efa2365c7860625fd2"
    response = requests.get(url)

    #print(response.text[10])
    data1=response.json()
    articles = data1.get('articles')
    titles=[]
    urlimage=[]
    urlsite=[]
    for i in articles:
        #print(i)
        if i['urlToImage'] and i['title'] is not None:
            l={'title':i['title'],'image':i['urlToImage'],'link':i['url']}
        # titles.append(i['title'])
        # urlimage.append(i['urlToImage'])
        # urlsite.append(i['url'])
        
            fullset.append(l)

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
    url =f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND sentiment.title.polarity:(negative neutral positive)&cursor=*&published_at.end=NOW&published_at.start=NOW-7DAYS/DAY'
    response = requests.get(url, headers=headers)
    data = response.json()
    data = data.get('stories')





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
    # Display summaries
    mydata=[]
    for i, summary in enumerate(preprocessed_text):
        # print(f"Summary for article {i + 1}:")
        # print("\nTITLE\n")
        # print(data[i]['title'])
        # print()
        d={'title':data[i]['title'],'summary':summary}
        mydata.append(d)
        # sentences = summary.split('. ')  # Split summary into sentences
        # for sentence in sentences:
        #     if sentence:
        #         print(f"- {sentence.strip()}")  # Print each sentence as a bullet point
        # print()

    return render(request,'Home.html',{'data':fullset,'mydata':mydata})


def user_register(request):
    fields = ['name', 'general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']
    if request.method == 'POST':
        # instance=User()
        print(request.POST)
        lastrec=User.objects.last()
        username='user'+str(lastrec.pk+1)
        user = User.objects.create_user(username=username,email=request.POST['email'], password=request.POST['password'])
        for field in fields:
            if field in request.POST:
                val = request.POST[field]
            else:
                val = False
            setattr(user, field, val)
        # lastrec=User.objects.last()
        # instance.username='user'+str(lastrec.pk+1)
        user.save()
        print(user)
        #instance.save() 
        return redirect('login')
    return render(request, 'signup.html',{})

def user_login(request):
    msg=''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Credentials are valid, proceed to login
            login(request, user)
            print(user)
            # Redirect to a success page or perform other actions
            return redirect('display-news')
    
    return render(request,'login.html',{'msg':msg})

@login_required(login_url="/login/")
def news_display(request):
    user=request.user
    #user_=User.objects.filter(user=user).first()
    user_=User.objects.filter(email=user).first()
    #user=get_user()
    print(user_)
    if user is not None:
        data=user.email
        print(data)
        print(user.business)
        user=User.objects.get(email=user)

        print(user)
        #print(user[2])
        load_dotenv()
        category=list()
        if user.business:
            category.append('business')
        if user.general:
            category.append('general')
        if user.entertainment:
            category.append('entertainment')
        if user.health:
            category.append('health')
        if user.science:
            category.append('science')
        if user.technology:
            category.append('technology')
        if user.sports:
            category.append('sports')
        random.shuffle(category)
        fields = [ 'general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']
        # for field in fields:
        #     if user[field]:
        #         category.append(field)
        print(category)
        fullset=[]
        for u in category:
            url = f"https://newsapi.org/v2/top-headlines?category={u}&country=in&apiKey=a965c9913dd043efa2365c7860625fd2"
            response = requests.get(url)

            #print(response.text[10])
            data1=response.json()
            articles = data1.get('articles')
            titles=[]
            urlimage=[]
            urlsite=[]
            for i in articles:
                #print(i)
                if i['urlToImage'] and i['title'] is not None:
                    l={'title':i['title'],'image':i['urlToImage']}
                # titles.append(i['title'])
                # urlimage.append(i['urlToImage'])
                # urlsite.append(i['url'])
                
                    fullset.append(l)
            #print(fullset)



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
        url =f'https://api.aylien.com/v6/news/stories?aql=language:(en) AND sentiment.title.polarity:(negative neutral positive)&cursor=*&published_at.end=NOW&published_at.start=NOW-7DAYS/DAY'
        response = requests.get(url, headers=headers)
        data = response.json()
        data = data.get('stories')





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
        # Display summaries
        mydata=[]
        for i, summary in enumerate(preprocessed_text):
            # print(f"Summary for article {i + 1}:")
            # print("\nTITLE\n")
            # print(data[i]['title'])
            # print()
            d={'title':data[i]['title'],'summary':summary}
            mydata.append(d)
            # sentences = summary.split('. ')  # Split summary into sentences
            # for sentence in sentences:
            #     if sentence:
            #         print(f"- {sentence.strip()}")  # Print each sentence as a bullet point
            # print()

        return render(request,'Home.html',{'data':fullset,'mydata':mydata})
    return render(request,'Home.html',{data:"NO USER"})

def logoutUser(request):
    logout(request)
    #return render(request,'Home.html',{})
    #return HttpResponseRedirect('home-view')
    return redirect('home-view')





