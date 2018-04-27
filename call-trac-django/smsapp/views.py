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
    return render(request, 'twilio/base.html')

def outgoing(request):
    return 1

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



