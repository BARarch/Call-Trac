import os
from twilio.rest import Client

accountSID = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']
twilioNum = os.environ['TWILIO_NUMBER']
auxNum = os.environ['AUX_NUMBER']

client = Client(accountSID, authToken)

client.messages.create(	
	to=auxNum,
	from_=twilioNum,
	body='How many robots do you count')

