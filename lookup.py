import os
from twilio.rest import Client

accountSID = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']

client = Client(accountSID, authToken)

number = client.lookups.phone_numbers('+14107882906').fetch()

print(number)