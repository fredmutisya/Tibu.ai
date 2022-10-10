#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install CoreNLP')


# In[ ]:


get_ipython().system('pip install textblob')


# In[ ]:


get_ipython().system('pip install spacy')
#if above doesn't work, try this in your terminal/ command


# In[ ]:


get_ipython().system('pip install nltk')
nltk.download()


# In[ ]:


get_ipython().system('pip install autocorrect')


# In[ ]:


get_ipython().system('pip install pyspellchecker')


# In[ ]:


get_ipython().system('pip install -U scikit-learn')


# In[ ]:


get_ipython().system('pip install tabula-py')


# In[1]:


import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import Word
import pandas as pd
import re
import numpy as np


# In[2]:


from autocorrect import Speller
from textblob import TextBlob
from spellchecker import SpellChecker


# In[3]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[71]:


#Loading two datasets, 
#spec is a list of specialists webscrapped from online resorces and pdfs by group 13
#symp is an open source diagnosis to symptom data set from kaggle from Pranay Patil (Owner)

spec = pd.read_excel('specialist list.xlsx')
symp = pd.read_csv('symptoms.csv')


# In[72]:


#clean the dataset
spec['PROVIDER'] = spec['PROVIDER'].str.lower()
spec['SPECIALTY'] = spec['SPECIALTY'].str.lower()
spec['COUNTY'] = spec['COUNTY'].str.lower()


# In[73]:


symp


# In[74]:


spec


# In[30]:


#Demo text- 'I have been having itchinnng and a rash'
#Intentionally mispell the words

sms_1 = 'I have been having some itchinnng and a rash'


# In[31]:


#The second sms is to elicit residence at the county level
#Use 'nairobi' as a test example

sms_2 = 'nairobi'


# In[32]:


#remove punctuations using regex
sms_1 = re.sub('[\,\.]', '', sms_1)


# In[33]:


#Tokenizing using regex to convert the sentense into individual words

sms_1 = re.split('\s+', sms_1)


# In[34]:


sms_1


# In[35]:


type(sms_1)


# In[36]:


#Convert it to a dataframe using pandas

sms_1_df =  pd.DataFrame({'sms_1':sms_1})


# In[37]:


sms_1_df


# In[38]:


#Removing stop words(words that carry no meaning)
#Use the dataframe made using pandas

#Removing stop words
stop = stopwords.words('english')

sms_1_df['sms_1_without_stop'] = sms_1_df['sms_1'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))


# In[39]:


sms_1_df


# In[40]:


sms1_final = sms_1_df['sms_1_without_stop'].apply(lambda x: str(TextBlob(x).correct()))


# In[41]:


#Drop the empty rows from the dataframe
pd.DataFrame(sms1_final)

nan_value = float("NaN")

sms1_final.replace("", nan_value, inplace=True)


# In[42]:


#Drop the empty rows from the dataframe with dropna

sms1_final = sms1_final.dropna(axis='index')


# In[43]:


print(sms1_final)


# In[44]:


sms1_final = list(sms1_final)


# In[45]:


sms1_final


# In[46]:


sms1_final[1]


# In[47]:


symp


# In[48]:


#Match the intents to the Kaggle data set

diagnosis = symp['Disease'].where((symp['Symptom_1'] == sms1_final[1]) & (symp['Symptom_2'] == sms1_final[2]))
    


# In[49]:


diagnosis


# In[50]:


diagnosis = diagnosis.dropna(axis='index')
diagnosis = diagnosis.drop_duplicates( keep = 'first')


# In[51]:


diagnosis


# In[52]:


diagnosis = list(diagnosis)


# In[53]:


diagnosis


# In[54]:


#import dataset that matches specialists and ICD 10 diagnoses

diag_spec = pd.read_csv("diag.spec.icd10.csv")


# In[55]:


diag_spec


# In[56]:


diagnosis[0]


# In[57]:


diagnosis[1]


# In[58]:


diagnosis[2]


# In[59]:


#Match the diagnosis
#Using using the top 3 options from diagnosis

specialist_1 = diag_spec['dgns_cd'].where((diag_spec['longdesc'] == diagnosis[0]))
specialist_2 = diag_spec['dgns_cd'].where((diag_spec['longdesc'] == diagnosis[1]))
specialist_3 = diag_spec['dgns_cd'].where((diag_spec['longdesc'] == diagnosis[2]))


# In[60]:


specialist_1 = specialist_1.dropna(axis='index')
specialist_1 = specialist_1.drop_duplicates( keep = 'first')
specialist_1


# In[61]:


specialist_2 = specialist_2.dropna(axis='index')
specialist_2 = specialist_2.drop_duplicates( keep = 'first')
specialist_2


# In[62]:


specialist_3 = specialist_3.dropna(axis='index')
specialist_3 = specialist_3.drop_duplicates( keep = 'first')
specialist_3


# In[77]:


#we will use loc from the pandas library to match the speciality with the diagnosis

reply_1 = spec.loc[(spec['SPECIALTY'] == 'dermatologist') & (spec['COUNTY'] == 'nairobi')]


# In[78]:


reply_1


# In[83]:


#reply1

print(f'\nHello, we have found {len(reply_1)} healthcare provividers/facilities that match your search for a dermatologist, reply Yes to get their location and contact details')


# In[ ]:


reply_2 = spec.loc[(spec['SPECIALTY'] == 'Physician') & (spec['COUNTY'] == 'nairobi')]


# In[ ]:


print(f'\nHello, we have found {len(reply_1)} facilities with  {specialist_1}s')


# In[ ]:


#If it fails to pick explictly, the chaot bot will ask for the acutal type of speciality the patient would like to see.


# In[ ]:


#The first sms is to elicit the specialty or service
#Use ambulance as a test example

sms = input("Hello, welcome to the mdoc health facility and provider finder, please state the type of specialist you wish to see: ")


# In[ ]:


sms = 'dentistry'


# In[ ]:


#This is an if statement that loops around the different professions which are broken into regex
#This is a quick method of stemming and lemmatization of the word
#the Intent is matched to choices available in our data set

if re.match(r'air.', sms):
    intent = 'air ambulance'
elif re.match(r'amb.', sms):
    intent = 'ambulance'
elif re.match(r'an(a|e).', sms):
    intent = 'anaesthesia'
elif re.match(r'ca.', sms):
    intent = 'cardiology'
elif re.match(r'coun.', sms):
    intent = 'counseling'
elif re.match(r'den.', sms):
    intent = 'dentistry'
elif re.match(r'der.', sms):
    intent = 'dermatologist'
elif re.match(r'endo.', sms):
    intent = 'endocrinology'
elif re.match(r'ent.', sms):
    intent = 'ENT Surgery'
elif re.match(r'fam.', sms):
    intent = 'family physician'
elif re.match(r'gas.', sms):
    intent = 'gastroenterology'
elif re.match(r'gen.', sms):
    intent = 'gentorologist'
elif re.match(r'gy.', sms):
    intent = 'gynaecology'
elif re.match(r'hem.', sms):
    intent = 'hemato-oncologist'
elif re.match(r'hom.', sms):
    intent = 'home care services'
elif re.match(r'hos.', sms):
    intent = 'hospital'
elif re.match(r'ima.', sms):
    intent = 'imaging services'
elif re.match(r'lab.', sms):
    intent = 'laboratory services'
elif re.match(r'neo.', sms):
    intent = 'neonatology'
elif re.match(r'nep.', sms):
    intent = 'nephrology'
elif re.match(r'n(e|u).', sms):
    intent = 'neurologist'
elif re.match(r'nutri.', sms):
    intent = 'nutritional services'
elif re.match(r'ob.', sms):
    intent = 'obstestrian'
elif re.match(r'oc.', sms):
    intent = 'occupational health specialist'
elif re.match(r'o(p|f).', sms):
    intent = 'ophthalmology'
elif re.match(r'max.', sms):
    intent = 'oral and maxillofacial surgeon'
elif re.match(r'ort.', sms):
    intent = 'orthopaedics'
elif re.match(r'onc.', sms):
    intent = 'oncology'
elif re.match(r'opt.', sms):
    intent = 'optical services'
elif re.match(r'path.', sms):
    intent = 'pathology'
elif re.match(r'p(a|e).', sms):
    intent = 'paediatrician'
elif re.match(r'physic.', sms):
    intent = 'physician'
elif re.match(r'physio.', sms):
    intent = 'physiotherapy services'
elif re.match(r'pl.', sms):
    intent = 'plastic surgeon'
elif re.match(r'ps.', sms):
    intent = 'psychiatry'
elif re.match(r'pul.', sms):
    intent = 'pulmonology'
elif re.match(r'rad.', sms):
    intent = 'radiologist'
elif re.match(r'rhe.', sms):
    intent = 'rheumatology'
elif re.match(r'sur.', sms):
    intent = 'general surgery'
elif re.match(r'ur.', sms):
    intent = 'urology'
else:
    print("Search inconclusive, could you describe your symptoms?.")	



#Check the intent in the list of healthcare facilities and specialities
#we will use loc from the pandas library to search for rows with both conditions

rslt_1 = spec.loc[(spec['SPECIALTY'] == intent) & (spec['COUNTY'] == 'nairobi')]

rslt_1

print(f'\nHello, we have found {len(rslt_1)} possible {intent} related service providers')


# In[ ]:


print(rslt_1)


# In[ ]:


#Once the FAQ comes online, we will use supervised learning from the corpus of FAQs
#We use TF-term frequency which is the ratio of the count of the word to the length of a sentence
#IDF -inverse document frequency is the log of the ratio of the No. total rows and the No. rows where the number is present

#tfidf_vectorizer = TfidfVectorizer()
#tfidf_matrix_symp = tfidf_vectorizer.fit_transform(symp)
#tfidf_matrix_sms1_final = tfidf_vectorizer.fit_transform(sms1_final)


# In[ ]:


#TD-IDF matrix. Each row represents a words from eye_symp
# Each column represents a unique word
#print(tfidf_matrix_symp)


# In[ ]:


#print(tfidf_matrix_sms1_final)


# In[ ]:


#Finding the similarity using the cosine similarity

#cosine_similarity(tfidf_matrix_eye, tfidf_matrix_sms1_final)


# In[ ]:





# In[ ]:




