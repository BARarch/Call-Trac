from django.shortcuts import render
from django.http import HttpResponseRedirect
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

from .models import MobileNumber, MobileMessage

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
@csrf_exempt
def app(request):
    message_form = SMSForm()
    data = get_messages()
    return render(request, 'twilio/base.html', {'form':message_form, 'messages':data})

def send(request):
    if request.method == 'POST':
        message_form = SMSForm(request.POST)

        if message_form.is_valid():
            print('__send: {}'.format(message_form.cleaned_data))
            name = message_form.cleaned_data['name']
            number = message_form.cleaned_data['number']
            message = message_form.cleaned_data['message']

            if is_valid_number(number):
                numberRecord = log_moble_number(number, name)
                send_message(message=message)
                log_message(numberRecord, message, True)
                print('Message Sent')
            else:
                message_form.add_error('number', 'not a valid number')
                print('Message Not Sent: not a valid number')
                data = get_messages()
                return render(request, 'twilio/base.html', {'form':message_form, 'messages':data})

    message_form = SMSForm()        
    return HttpResponseRedirect('/rerender/')

@csrf_exempt
def sms(request):
    if request.method == 'POST':
        query = request.POST
        number = query['From']
        messageText = query['Body']

        print('\nThere was a message from: {}'.format(number))
        print('...and it said: {}\n'.format(messageText))

        
        numberRecord = log_moble_number(number=number)
        log_message(numberRecord, messageText, False)

        #message_form = SMSForm()

    return HttpResponseRedirect('/rerender/')

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

def log_moble_number(number=AUX_NUMBER, name='NONE'):
    numberRecord = MobileNumber.objects.filter(phone=number)
    if numberRecord:
        numberRecord = numberRecord[0]
    else:
        numberRecord = MobileNumber(phone=number, name=name)
        numberRecord.save()
    return numberRecord

def log_message(numberRecord, body, sent):
    MobileMessage(number=numberRecord, body=body, sent=sent).save()


def get_messages():
    result = MobileMessage.objects.all()
    return result





