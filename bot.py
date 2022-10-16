from flask import Flask
from flask import request
from flask import Response
from hackathon_chat_symptoms import *
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
        if txt == 'Hey':
            tel_send_message(chat_id,'Hello, welcome to Tibu.ai')
        elif txt == 'Nairobi':
            tel_send_message(chat_id,diag)
        else:
            try:
                diag = get_specialists(make_diagnosis(txt))
                diagnosis_text = ','.join(make_diagnosis(txt))
                tel_send_message(chat_id,'Hi there, from the brief description of your symptoms, possible diagnoses could be '+diagnosis_text+'. If you want suggestions on possible specialists in your area, please indicate your county of residence')
            except:
                tel_send_message(chat_id,'Whoops! We are still working to support your query')
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)