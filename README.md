# Tibu.ai
Group 13 Microsoft/mdoc/ALA Hackthon presentation(Use Jupyter notebook file(hackathon chat symptoms.ipynb) for best experience)


This is a rule based chat bot made using python

Patients have a challenge in knowing the specialty type that matches
their symptoms. There are over 1000 specialists in Kenya and web
based searches can link them to unqualified health care specialists.

Challenge:
Users would like to receive suggestions on recommended healthcare
facilities or providers based on their symptoms, diagnosis or results
from previous FAQs by other users.





Functionality stages
Stage 1-
Recommending a facility/provider based on symptoms.
Recommending a facility/provider based on specialty name as a redundancy

Stage 2-
Recommending a facility/provider based on location.

Stage 3-
Recommending a facility/provider based on insurance type.
Recommending a facility/provider based on opening times and days.



We have 3 datasets
1. specialist.xlsx
A health speciality and health facility database which has over 13,000 health facilities and specialities of different levels with details on
Names e.g., Mukavakava
Level of care e.g., Level 2
Facility type e.g., Dispensary or Dermatology
Ownership e.g, MOH
Opening times and days
Geodata e.g., Kakamega county, Malava constituency, Malava sub-county, Butali ward.
Number of Beds e.g., One
Insurance providers accepted e.g. CIC(Only one providers data uploaded, more to follow)

2. symptoms.csv
This is a Kaggle dataset from Pranay Patil (Owner) with diagnosis and possible symptoms. Further editing of this dataset is needed.

3. diag.spec.icd10.csv
This is a modified dataset from ICD10 which is a international classification system for diseases used in all countries. Our health care experts in Group 13 matched diagnoses with specialities. More editing of this dataset would be needed.

PYTHON LIBRARIES
Tibu.ai makes use of the following  libraries in python.

pandas-manipulate dataframes
nltk-Natural language toolkit-
removing stop words and stemming words
Textblob-word processing
re-regular expressions
sklearn-text- text classification
autocorrect-spelling corrector
openpyxl-read/write excel


TEXT PREPROCESSING 
Tibu.ai will tokenize the sentence into words.
Tibu.ai then removes punctuations and stop words using regular expressions. We then macth the symptoms with the diagnosis dataset. From the diagnosis dataset we match the diagnosis to Tibu.ai's curated list of medical specialist and health care facilities.

The result is then provided to the client 

Ground work for transistioning from a rule based chat bot to a machine learning chatbot will be done once the corpus of FAQs and responses is large enough.

Authors- Group 13
