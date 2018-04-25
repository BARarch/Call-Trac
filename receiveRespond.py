from flask import Flask, request
from twilio import twiml
import sendTxt as st
 
 
app = Flask(__name__)
 
 
@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    print(number)
    print(message_body)
 
    
    st.send_message(number,'Hello {}, you said: {}'.format(number, message_body))
    print('Reply Sent')
    return 'Done'
 
if __name__ == '__main__':
    app.run(port=8000)