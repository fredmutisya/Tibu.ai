from flask import Flask
from flask import request
from flask import Response
from hackathon_chat_symptoms import *
from bot_commands import *
import requests
 
TOKEN = "5724165243:AAHXbboth6Z2vaeQ19LZ3IBNy2Yk7zd8sK4"
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    global diag
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        print(classify_message(txt))
        if txt == "/start":
            tel_send_message(chat_id,answer_greeting())
        if classify_message(txt) == 1:
            tel_send_message(chat_id,answer_greeting())
        elif classify_message(txt) == 2:
            try:
                tel_send_message(chat_id,get_a_specialist(chat_id,txt))
            except:
                tel_send_message(chat_id,"Sorry. I dint get that. Try Again.")
        else:
            try:
                set_diagnosis(chat_id,txt)
                tel_send_message(chat_id,reply_diagnosis(get_diagnosis(chat_id))) 
            except:
                tel_send_message(chat_id,"How are you feeling?") 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)