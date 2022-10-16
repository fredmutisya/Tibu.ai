from hackathon_chat_symptoms import *

message_type = 0 #  0 is a diagnosis text , 1 is a greeting, 2 is a county

county_list = ['nairobi','mombasa','meru']
greetings = ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"]

diagnosis_list = [[121,'Heartache'], [145,'Toothache']]

global patient_diagnosis

def answer_greeting():
    return('Hello. Welcome to Tibu AI, please describe what you are feeling or specify a physician you would like to see')

def set_diagnosis(chat, userMessage):
    diagnosis_list.append([chat,make_diagnosis(userMessage)])

    #print(make_diagnosis(userMessage))

   
def get_diagnosis(chat):
    for id in range(len(diagnosis_list)):
        if diagnosis_list[id][0] == chat:
            patient_diagnosis = diagnosis_list[id][1]
    
    return(patient_diagnosis)

def get_a_specialist(chat,location):
    diag = get_diagnosis(chat)
    return(get_specialists(diag, location))


def classify_message(text):
    try:
        county_list.index(str.lower(text))
        message_type = 2
    except:
        message_type = 0


    if message_type == 0:
        try:
            greetings.index(str.lower(text))
            message_type = 1
        except:
            message_type = 0
     
    return(message_type)

def reply_diagnosis(diag):
    diagnosis_text = ','.join(diag)
    reply = 'Hi there, from the brief description of your symptoms, possible diagnoses could be '+diagnosis_text+'. If you want suggestions on possible specialists in your area, please indicate your county of residence'
    return(reply)

