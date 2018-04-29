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
from twilio.rest import Client

TWILIO_ACCT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_CHAT_SID = os.environ['TWILIO_CHAT_SID']
TWILIO_SYNC_SID = os.environ['TWILIO_SYNC_SID']
TWILIO_API_SID = os.environ['TWILIO_API_SID']
TWILIO_API_SECRET = os.environ['TWILIO_API_SECRET']

TWILIO_CLIENT = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

# Create your views here.

class SMSFormView(FormView):
    form_class = SMSForm
    template_name = 'twilio/base.html'
    success_url = '/message-sent/'

    def form_invalid(self, form):
        response = super(SMSFormView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(SMSFormView, self).form_valid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

def app(request):
    message_form = SMSForm()
    return render(request, 'twilio/base.html', {'form':message_form})

def send(request):
    if request.method == 'POST':
        message_form = SMSForm(request.POST)

        if message_form.is_valid():
            print('__send: {}'.format(message_form.cleaned_data))
            print(TWILIO_ACCT_SID)

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


def token(request):
    fake = Factory.create()
    return generateToken(fake.user_name())

def generateToken(identity):
    # Credetials from Environment Vars
    account_sid = settings.TWILIO_ACCT_SID
    chat_service_sid = settings.TWILIO_CHAT_SID
    sync_service_sid = settings.TWILIO_SYNC_SID
    api_sid = settings.TWILIO_API_SID
    api_secret = settings.TWILIO_API_SECRET

    print('Account Sid :{}:'.format(account_sid))
    print('Chat Sid :{}:'.format(chat_service_sid))

    print

    # Create access token
    token = AccessToken(account_sid, api_sid, api_secret, identity=identity)

    # Create sync grant
    if sync_service_sid:
        sync_grant = SyncGrant(service_sid=chat_service_sid)
        token.add_grant(sync_grant)

    if chat_service_sid:
        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    print('there was a token generated for {}'.format(identity))

    return JsonResponse({'identity':identity, 'token':token.to_jwt().decode('utf-8')})



