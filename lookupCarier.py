import os
from twilio.rest import Client

accountSID = os.environ['TWILIO_ACCOUNT_SID']
authToken = os.environ['TWILIO_AUTH_TOKEN']

client = Client(accountSID, authToken)

number = client.lookups.phone_numbers('+12212212221').fetch(type='carrier')

print(number.carrier['name'])

def is_valid_number(number):
    try:
        response = client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e