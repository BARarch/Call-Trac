import os
from twilio.rest import Client

accountSID = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']
twilioNum = os.environ['TWILIO_NUMBER']
auxNum = os.environ['AUX_NUMBER']

client = Client(accountSID, authToken)

def send_message(number=auxNum, message='Default Message says Hello'):
    client.messages.create(
        to=number,
        from_=twilioNum,
        body=message)


if __name__ == '__main__':

    client.messages.create( 
        to=auxNum,
        from_=twilioNum,
        body='How many robots do you count')

