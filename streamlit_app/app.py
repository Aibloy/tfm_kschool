# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:27:48 2020

@author: Willi
"""

# Twitter Scrapper

# !streamlit run app.py

import streamlit as st
import tweepy as tw
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import re
from PIL import Image
from urllib.request import urlopen
import pickle 
from Utilities.LIWC_EN  import LIWC_ENGLISH
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

from nltk.corpus import stopwords 
stop_words = list(set(stopwords.words('english'))) + ["enlace","mencion"]

pd.set_option('display.max_rows', 500)
# pd.set_option('display.width', 1000)
#.............................................................................................................
#.............................................................................................................
#.............................................................................................................
#.............................................................................................................

with open("api_keys.txt","r") as file:      #Las claves deben estar en el archivo .txt
    for line in file:
        exec(line)
    claves = tw.OAuthHandler(consumer_key, consumer_secret)
    claves.set_access_token(access_token, access_token_secret)
    api = tw.API(claves, wait_on_rate_limit=True)
#.............................................................................................................
@st.cache
def get_tweets(user,N=200):
    """ Obtener -al menos- N Tweets de un usuario"""
    try: # Si el usuario no existe o es privado:
        tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, tweet_mode='extended')
        corpus = [tweet.full_text for tweet in tweets]
        picture = [x.user.profile_image_url for x in tweets][0]


    except:
        corpus = None
        picture = None

    return corpus, picture
#.............................................................................................................
@st.cache    
def load_picture(url):
    url.replace("normal","bigger")
    img = Image.open(urlopen(url))
    return img
#.............................................................................................................
def clean_text_english(x):
    x = x.lower()
    x = re.compile('htt\S+').sub(' enlace ',x)
    x = re.compile('@\S+').sub(' mencion ',x)
    x = re.compile('#\S+').sub(' hashtag ',x)
    x = re.sub(r"[^a-zA-Z.]", ' ', x)   
    x = re.sub(r" +", ' ', x)
    return x
#.............................................................................................................
def clean_list(x):
    return x.split("(")[1].replace(")","")
#.............................................................................................................
@st.cache
def models():
    modelos = pickle.load( open("Utilities/modelos/modelos_english.pkl", "rb" ) )
    return modelos
modelos = models()
#.............................................................................................................
def code_text(text):
    with open("Utilities/modelos/features_english.pkl", "rb" ) as f:
            features = pickle.load(f)
    vect = CountVectorizer(vocabulary=features, ngram_range=(1,3), max_features=5000)
    X = vect.fit_transform([text])
    X = pd.DataFrame(X.toarray(), columns = features)
    return X
#.............................................................................................................
def get_personality(text):
    """ vector: e i n s f t j p"""
    vector = []
    text_coded = code_text(text)
    for i in range(4):
        model = modelos[i]
        y_pred = model.predict_proba(text_coded)[0]
        vector.append(y_pred[0])
        vector.append(y_pred[1])
    return vector
#.............................................................................................................
def get_descriptions(df):
    with open("Utilities/descriptions.pkl","rb") as f:
        descriptions= pickle.load(f)
    df = df[df["value"]>0.5]["type"]
    devolver = []
    for i in df:
        devolver.append(descriptions[i])
    return "\n\n".join(devolver)
#.............................................................................................................
def create_wordcloud(text):
    wordcloud = WordCloud(stopwords=stop_words,background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()
#.............................................................................................................
def plot_radar(vector):
    "ipfnejts"
    vector = [vector[1],vector[7],vector[4],vector[2],vector[0],vector[6],vector[5],vector[3]] # Ordenar vector manualmente para que encaje con la salida del modelo
    df = pd.DataFrame({'type': "INTROVERSION PERCEIVING FEELING INTUITION EXTROVERSION JUDGING THINKING SENSING".title().split(),
                   'value':vector})
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="polar")
    
    theta = np.arange(len(df) + 1) / float(len(df)) * 2 * np.pi
    values = df['value'].values
    values = np.append(values, values[0])
    
    l1, = ax.plot(theta, values, color="C2", marker="o", label="Name of Col B")
    plt.xticks(theta[:-1], df['type'], color='black', size=15)
    ax.tick_params(pad=50) # to increase the distance of the labels to the plot
    
    ax.fill(theta, values, 'green', alpha=0.1)
    st.pyplot()
    st.write(df[df["value"]>0.5])
    st.header("Description of the personality of this User: ")
    st.write(get_descriptions(df))
    
    return df
#.............................................................................................................
#.............................................................................................................
#.............................................................................................................
#.............................................................................................................
st.sidebar.header("By William Sanz Vivanco")
C = st.sidebar.button("GITHUB REPOSITORY")
if C:
    st.sidebar.markdown("[github repository](https://github.com/Aibloy/tfm_kschool)")
I = st.button("Introduction")
if I:
    st.header("Master thesis")
    
    st.markdown("""
This project is part of my master's project in Data Science at K-School

The app has been created with Streamlit, it can predict the personality based on the MBTI model 

**¿How to use it?**


Select the way that you will use for get the data, you can writte it manually or export data from Twitter 
specifying a user account
""")
    R = st.button("Hide Introduction")
    if R:
        del I 
#.............................................................................................................
#.............................................................................................................        
I = st.button("¿What is MBTI?")
if I:
    st.image(Image.open("Utilities/mbti_image.png"))
    st.markdown("""
The Myers Briggs Type Indicator (or MBTI for short) is a personality type model that divides the personality in four dimensions:

> **Introversion (I) – Extroversion (E)**

> **Intuition (N) – Sensing (S)**

> **Thinking (T) – Feeling (F)**

> **Judging (J) – Perceiving (P)**

Each dimension tries to explain the way a person processes their life. In order:
- how we interact with our surroundings
- how we see the world and process information
- how we make decisions and cope with emotionS
- Our approach to work, planning and decision-making
""")
    R = st.button("Hide")
    if R:
        del I 

#.............................................................................................................
I = st.button("¿How it works?")
if I:
    st.markdown("""
The model (LGBM) is based in tree based learning algorithms with gradient boosting framework and has been
trained with  hundreds of miles of texts in english from almost 20 thousand different users,
the texts were coded in a simple bag of words with n-grams, specifically: max_features=5000, ngram_range(1,3)
""")
    R = st.button("Hide")
    if R:
        del I 
#.............................................................................................................

clean_corpus = None

d = ["Twitter Account","Writte manually"]
origen = st.radio("Select way to get texts for analysis :",tuple(d))
# st.write(modelos)
    
if origen == d[0]: # TWITTER ACCOUNT
    st.markdown("- The username must be public")
    st.markdown("- The language of user must be English")
    entrada = st.text_input("Twitter username :")
        
    if entrada and len(entrada.split())==1:
        corpus,picture = get_tweets(entrada,200)
        

        if corpus != None :
            clean_corpus = [clean_text_english(x) for x in corpus]
            clean_corpus = [x for x in clean_corpus if len(x) >3]
            clean_corpus = " ".join(clean_corpus)
            st.markdown(">**DONE:** ")           
            st.image(load_picture(picture), width=100)
            st.write(f"Collected last {len(corpus)} tweets from {entrada} with {len(clean_corpus.split())} words and {len(set(clean_corpus.split()))} unique words")   
            if st.checkbox("Show Tweets collected :"):
                st.write(corpus)
            if st.checkbox("Show clean data :"):
                st.write(clean_corpus)
        else: 
            st.markdown(">**ERROR: The user doesn't exists or the account is private, otherwise the twitter api has made restrictions, try again later or with a different user**")
    #else:
        #st.markdown(">**ERROR: The user doesn't exists or the account is private**")
            
                
if origen == d[1]:  # WRITTE MANUALLY
    entrada = st.text_input("Write something")
    if entrada:
        clean_corpus = clean_text_english(entrada)
        
if clean_corpus!=None:
    st.header(f"**{entrada.upper()}** MBTI PERSONALITY TYPE")
    create_wordcloud(clean_corpus)
    vector = get_personality(clean_corpus)
    tipo = plot_radar(vector)
    


    
    #..................................................................................................LIWC ANALYSIS
    LIWC = LIWC_ENGLISH([clean_corpus]).T.sort_values(by=0,ascending=False)
    LIWC.index = [clean_list(x) for x in LIWC.index]
    liwc_features = LIWC[LIWC[0]!=0].reset_index()["index"]
    LIWC_filtrado = LIWC.sort_values(by=0, ascending=False).reset_index().drop(0,axis=1)
    #LIWC_filtrado["index"] = LIWC_filtrado["index"].apply(clean_list)
        
        
        
    if st.checkbox("Show LIWC analysis"):
        st.title("LIWC ANALYSIS")
        if st.button("¿What is LIWC?"):
            st.write("""
The way that the Linguistic Inquiry and Word Count (LIWC) program works is fairly simple. Basically, it reads a given text and counts the percentage of words that reflect different emotions, thinking styles, social concerns, and even parts of speech. 

Because LIWC was developed by researchers with interests in social, clinical, health, and cognitive psychology, the language categories were created to capture people’s social and psychological states.
                         """)
            st.markdown("Oficial Website: http://liwc.wpengine.com")
                
        st.markdown("The LIWC categories ordered from the most used  to the least with the actual data")
        # st.write(LIWC_filtrado["index"])
        st.write(LIWC)
            
        if st.checkbox("Filter categories in LIWC for see specific positions"):
            categories_selected = st.multiselect("Select features", liwc_features)
                
            st.write(LIWC_filtrado[LIWC_filtrado["index"].isin(categories_selected)])
    
