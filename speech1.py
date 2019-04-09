# coding: utf-8

# # Meet Robo: your friend
from twilio.rest import Client
import nltk
import warnings
warnings.filterwarnings("ignore")
import speech_recognition as sr
import csv

account = "Enter account key here"

token = "Enter token key here"


# nltk.download() # for downloading packages

import numpy as np
import random
import string # to process standard python strings

client = Client(account, token)

f=open('Hotelbot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words


sent_tokens[:2]


word_tokens[:5]


lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]



# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("Welcome to our site, if you need help simply reply to this message, we are online and ready to help. If you want to exit, type Bye!")
print("Do you want to provide a review or chat with our executive")
a=input("Enter a value")
if a=="1":
    row1=[]
    with open('dataset_2.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        r = sr.Recognizer()
        f= open("hotel.txt","a+")
        rid = input("Review Id")
        row1.append(rid)
        uid = input("User Id")
        row1.append(uid)
        bid = input("Business Id")
        row1.append(bid)
        stars = input("Stars")
        row1.append(stars)
        date = input("Date")
        row1.append(date)
       
        with sr.Microphone() as source:
            print("Give your feedback on your overall experience :")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("You said : {}".format(text))
                f.write(text)
                rev=text
                row1.append(text)
                useful = input("Service")
                row1.append(useful)
                funny = input("Ambience")
                row1.append(funny)
                cool = input("Locality")
                row1.append(cool)
                writer.writerow(row1)
                #f.write("\n")
            except:
                print("Sorry could not recognize what you said")
                writer.writerow(row1)
        f.close()
        csvFile.close()

else:
    while(flag==True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please ask a question :")
            audio = r.listen(source)
            try:
                user_response = r.recognize_google(audio)
                print("You said : {}".format(user_response))
                #user_response = input()
                user_response=user_response.lower()
                if(user_response!='bye'):
                    if(user_response=='thanks' or user_response=='thank you' ):
                        flag=False
                        print("Admin: You are welcome..")
                    else:
                        if(greeting(user_response)!=None):
                            print("Admin: "+greeting(user_response))
                        else:
                            print("Admin: ",end="")
                            user_response1=response(user_response)
                            #print(response(user_response))
                            print(user_response1)
                            sent_tokens.remove(user_response)
                            if user_response1!="":
                                print("---->>>message")
                                message = client.messages.create(to="+919940615198", from_="+16184946168",body=user_response1)
                                #message = client.messages.create(to="+919910275909", from_="+19733584440",body=user_response1)
                                print(message)
                else:
                    flag=False
                    print("Admin: Bye! take care..")

            except:
                print("Sorry could not recognize what you said")
        
