from tkinter import *
import sys
import random
import string
import nltk
import numpy as np


nltk.download('punkt')
nltk.download('wordnet')



f=open('college.txt','r',errors="ignore")
raw_data=f.read().lower()
sent_tokens = nltk.sent_tokenize(raw_data)
word_tokens = nltk.word_tokenize(raw_data)

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["Hi", "Hey", "*nods*", "Hi there", "Hello", "I am glad! You are talking to me"]

CLOSING_INPUTS= ("bye", "thank you!", "goodbye", "see ya!")
CLOSING_RESPONSES= ["Bye","Thank you","Goodbye","See ya!","Have a nice day"]



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response():
    user=e.get().lower();
    if user in GREETING_INPUTS:
        text.insert(END,'\n'+'[YOU]: '+user.upper())
        text.insert(END,'\n'+'[BOT]: '+random.choice(GREETING_RESPONSES))
        e.delete(0,END)
    elif user in CLOSING_INPUTS:
        text.insert(END,'\n'+'[YOU]: '+user.upper())
        text.insert(END,'\n'+'[BOT]: '+random.choice(CLOSING_RESPONSES).upper())
        e.delete(0,END)
        root.after(1000,root.destroy)
    else:
        robo_response=''
        sent_tokens.append(user)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you".upper()
            text.insert(END, '\n'+'[YOU]: ' + e.get().upper())
            text.insert(END,"\n"+'[BOT]: '+robo_response.upper())
            robo_response=''
            e.delete(0,END)
        else:
            robo_response = robo_response+sent_tokens[idx]
            text.insert(END, '\n'+'[YOU]: ' +e.get().upper())
            text.insert(END, "\n" + '[BOT]: ' + robo_response.upper())
            robo_response=''
            e.delete(0, END)


root=Tk()
root.title('College And Student Query Bot')
photo=PhotoImage(file='logo.png')
root.iconphoto(False,photo)
root.resizable(0,0)
text=Text(root,wrap=WORD,bd=5,width=100)
text.grid(row=0, column=0,columnspan=6)
e=Entry(root,width=100,bg='orange',bd=5,font='Lucida 10 bold')
text.insert(END,'\n'+'[BOT]: '+random.choice(GREETING_RESPONSES)+',How may I help you?')
send=Button(root,text='Send',bg='blue',command=response,width=12).grid(row=1,column=1)
e.grid(row=1,column=0)

root.mainloop()