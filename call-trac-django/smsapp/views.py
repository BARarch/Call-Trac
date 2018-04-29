from django.shortcuts import render
from django.views.generic import FormView
from .forms import SMSForm

from faker import Factory
from django.http import JsonResponse
from django.conf import settings

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)

from django.views.decorators.csrf import csrf_exempt

import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


TWILIO_ACCT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_CHAT_SID = os.environ['TWILIO_CHAT_SID']
TWILIO_SYNC_SID = os.environ['TWILIO_SYNC_SID']
TWILIO_API_SID = os.environ['TWILIO_API_SID']
TWILIO_API_SECRET = os.environ['TWILIO_API_SECRET']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
AUX_NUMBER = os.environ['AUX_NUMBER']

TWILIO_CLIENT = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

# Create your views here.

def app(request):
    message_form = SMSForm()
    return render(request, 'twilio/base.html', {'form':message_form})

def send(request):
    if request.method == 'POST':
        message_form = SMSForm(request.POST)

        if message_form.is_valid():
            print('__send: {}'.format(message_form.cleaned_data))
            number = message_form.cleaned_data['number']
            message = message_form.cleaned_data['message']

            if is_valid_number(number):
                send_message(message=message)
                print('Message Sent')
            else:
                print('Message Not Sent: not a valid number')

    message_form = SMSForm()        
    return render(request, 'twilio/base.html', {'form':message_form})

@csrf_exempt
def sms(request):
    if request.method == 'POST':
        query = request.POST
        print('\nThere was a message from: {}'.format(query['From']))
        print('...and it said: {}\n'.format(query['Body']))
        message_form = SMSForm()
        
    return render(request, 'twilio/base.html', {'form':message_form})


def is_valid_number(number):
    try:
        response = TWILIO_CLIENT.lookups.phone_numbers(number).fetch(type="carrier")
        print('__sendCarrier: {}'.format(response.carrier))
        if response.carrier['type'] == 'mobile':
            return True
        else:
            return False
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

def send_message(number=AUX_NUMBER, message='Default Message says Hello'):
    TWILIO_CLIENT.messages.create(
        to=number,
        from_=TWILIO_NUMBER,
        body=message)


