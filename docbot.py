#*******CREATING THE CHATBOT LOGIC USING PYTHON LIBRARIES*********** 

#******Importing Natural language toolkit and other packages*******
import nltk
import warnings
warnings.filterwarnings("ignore")

#*****Importing Numpy used for dealing with multi-dimensional arrays and matrices********* 
import numpy as np

#******Importing random library to generate random numbers**********
import random

#******Importing string library to process standard python strings*******
import string 

#******Opening disease and doctor files****************
f=open('disease.txt','r',errors = 'ignore')
m=open('doctor.txt','r',errors = 'ignore')
checkpoint = "./chatbot_weights.ckpt"

#******Reading the disease and doctor file and storing in variable*******
raw=f.read()
rawone=m.read()
raw=raw.lower()# converts to lowercase
rawone=rawone.lower()# converts to lowercase

#*******Download the punkt(sentence tokenizer) and wordnet(Lexical database)*******
nltk.download('punkt') 
nltk.download('wordnet') 


#******************TOKENIZATION*********************

#*******Converts to the list of sentences*********
sent_tokens = nltk.sent_tokenize(raw)

#*******Converts to the list of words**********
word_tokens = nltk.word_tokenize(raw)

#*******Converts to the list of sentences*********
sent_tokensone = nltk.sent_tokenize(rawone)

#*******Converts to the list of words**********
word_tokensone = nltk.word_tokenize(rawone)


sent_tokens[:2]
sent_tokensone[:2]

word_tokens[:5]
word_tokensone[:5]

#***************LEMMATIZATION*************
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



#**************Providing greetings and initial texts***************
Introduce_Ans = [" "]
GREETING_INPUTS = ("hello", "hi","hey", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["I am glad you are talking to me, so tell me are you facing any health issues?"]
Basic_Q = ("yes","y")
Basic_Ans = "okay, Don't worry tell me about your symptoms"
Basic_Om = ("no","n")
Basic_AnsM = ["It's okay, thank you for using our service. Visit again if you need any help"]
fev=("fever","i have fever","I am suffering from fever")
feve_r=("Which type of fever you have? Please mention other side symptoms as well so we try to calculate your disease.")


# **********Checking for greetings**************
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# **********If user entered Yes i.e. feeling sick**********
def basic(sentence):
    for word in Basic_Q:
        if sentence.lower() == word:
            return Basic_Ans
def fever(sentence):
    for word in fev:
        if sentence.lower() == word:
            return feve_r

# ************If user entered No i.e. not feeling sick*********
def basicM(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in Basic_Om:
        if sentence.lower() == word:
            return Basic_AnsM
            
           #print(random.choice(Basic_AnsM))
            return exit()

# Used for Introduction
def IntroduceMe(sentence):
    return random.choice(Introduce_Ans)


#**********USING Cosine Similarity and TF-IDF for dealing woth words in generating docbot responses**************
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# *********Generating appropriate response by the chatbot****************
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
        robo_response=robo_response+"I am sorry! I didn't understand you. Can you be more clear?"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx] 
        return robo_response
      

# **********Generating response*************
def responseone(user_response):
    robo_response=''
    sent_tokensone.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokensone)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I didn't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokensone[idx]
        return robo_response

#**************Function to deal with fetching user responses and extracting approriate chatbot reply.
def chat(user_response):
    user_response=user_response.lower()
    keyword = " module "
    keywordone = " module"
    keywordsecond = "module "
    
    if(user_response!='bye'):
        
        if(user_response=='thanks' or user_response=='thank you ' ):
            flag=False
            return "You are welcome."
        elif(basicM(user_response)!=None):
            return basicM(user_response)
        else:
            if(user_response.find(keyword) != -1 or user_response.find(keywordone) != -1 or user_response.find(keywordsecond) != -1):
                return responseone(user_response)
                sent_tokensone.remove(user_response)
            elif(greeting(user_response)!=None):
                return greeting(user_response)
            elif(user_response.find("your name") != -1 or user_response.find(" your name") != -1 or user_response.find("your name ") != -1 or user_response.find(" your name ") != -1):
                return IntroduceMe(user_response)
            elif(basic(user_response)!=None):
                return basic(user_response)
            elif(fever(user_response)!=None):
                return fever(user_response)
            else:
                return response(user_response)
                sent_tokens.remove(user_response)
                
    else:
        flag=False
        return "Bye! Thank you. Take care. "
        


