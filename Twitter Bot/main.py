from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pickle
import tweepy
import csv
import pandas as pd
import time
from keras.models import load_model
import json
import nltk
import random
import string, re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

from flask import jsonify
from flask_wtf.csrf import CSRFProtect
from flask import request
from flask import  Flask,render_template
app=Flask(__name__)

consumer_key = 'Iq2hUDTuDhPxDzFMdfRY2ydrw'
consumer_secret = 'VLmdRXhB7CS3yZQNepRUkojdpRrtKj6xO2Kd9JEPmVWnPQBo0m'
access_token = '1353947976939393024-bmaiuLpuIPtYiecJHnpxUfqA97fJSV'
access_token_secret = 'K48HO2rU9zx38X5MaFoFETwcwqk4qeRPvpUtCjAUznvop'



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

current_date = time.strftime("%Y-%m-%d")


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


@app.route('/')
def index():    
    return render_template("index.html")

@app.route('/reply', methods=['POST'])
def reply():
    json_request = request.json
    text = json_request['msg']
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return jsonify(text=res)

@app.route('/tweetDisplayByKeyword', methods=['POST'])
def tweetDisplayByKeyword():
    json_request = request.json
    text = json_request['msg']
    tweets = []
    times = []
    for tweet in tweepy.Cursor(api.search, q=text+" -filter:retweets", count=2, lang="en", since=current_date, tweet_mode="extended").items(10):
        print (tweet.created_at, tweet.full_text)
        cleaned_tweet_text = re.sub(r"(?:\@|https?\://)\S+", "", tweet.full_text) #remove web links
        cleaned_tweet_text = re.sub('&amp;', '&', cleaned_tweet_text) #remove web links
        tweets.append(cleaned_tweet_text)
        times.append(tweet.created_at)
    return jsonify(time=times, text=tweets)

@app.route('/tweetDisplayByAccount', methods=['POST'])
def tweetDisplayByAccount():
    json_request = request.json
    text = json_request['msg']
    tweets = []
    times = []
    for tweet in tweepy.Cursor(api.user_timeline, q="-filter:retweets", id=text, count=2, lang="en", since=current_date, include_rts=False, tweet_mode="extended").items(10):
        print (tweet.created_at, tweet.full_text)
        cleaned_tweet_text = re.sub(r"(?:\@|https?\://)\S+", "", tweet.full_text) #remove web links
        cleaned_tweet_text = re.sub('&amp;', '&', cleaned_tweet_text) #remove web links
        tweets.append(cleaned_tweet_text)
        times.append(tweet.created_at)
    return jsonify(time=times, text=tweets)

if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True)