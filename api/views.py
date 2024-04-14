from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from api.utils.HashUtils import HashUtils
from api.utils.JwtAuth import JwtAuth

from . import models
from . import forms

from uuid import uuid4
import json

#csrf "revogation"
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
#@method_decorator(csrf_exempt)

def api_register(request):
    if request.method == 'POST':
        form = forms.UserSignInForm(request.POST)

        if form.is_valid():
            try:
                query = models.User.objects.get(email=form.cleaned_data['email'])

                context = {
                    'response': 402,
                    'message': 'Email already used.'
                    }

                url = reverse('index') + f'?context={context}'
                return redirect(f'/?message={context["message"]}')
            
            except models.User.DoesNotExist:

                hash_n_salt = HashUtils().generate_n_hash(form.cleaned_data['password'])

                user = models.User(
                    user_name=form.cleaned_data['user_name'],
                    email=form.cleaned_data['email'],
                    password_hash=hash_n_salt['password'],
                    salt=hash_n_salt['salt']
                )

                try:
                    user.save()
                except IntegrityError:
                    context = {
                            "response": 402,
                            "message": 'Email already used.'
                        }
                    
                    url = reverse('index') + f'?context={context}'
                    return redirect(f'/?message={context["message"]}')

                context = {
                            "response": 200,
                            "message": "User sign in successful"
                        }

                return redirect(f'/?message={context["message"]}')
        
        else:
            context = {
                        "response": 401,
                        "message": 'Invalid data.'
                    }

            return redirect(f'/?message={context["message"]}')

    context = {
                "response": 401,
                "message": f"Invalid http method, don't use {request.method}"
            }

    return redirect(f'/?message={context["message"]}')


def api_login(request):
    if request.method == 'POST':

        form = forms.UserLogInForm(request.POST)

        if form.is_valid():
            try:
                query = models.User.objects.get(email=form.cleaned_data['email'])

                query = query.to_dict()
                
                user_password = HashUtils().encrypt(form.cleaned_data['password'], query['salt'])

                if str(user_password) == query['password_hash']:
                    
                    user_data = {
                        "user_id": query['user_id'],
                        "user_name": query['user_name'],
                        "email": form.cleaned_data['email']
                    }

                    with open('private_key.pem', 'r') as f:
                        private_key = f.read()

                    token = JwtAuth().generate_token(user_data, private_key)
                
                    context = {
                                "response": 200,
                                "message": "User log in successful",
                                "token": token
                            }

                    request.session['user_token'] = str(token)

                    return redirect(f'/?message={context["message"]}')

                else:
                    context = {
                                "response": 401,
                                "message": "Wrong credentials."
                            }

                    return redirect(f'/?message={context["message"]}')
            
            except models.User.DoesNotExist:
                context = {
                            "response": 404,
                            "message": "User was'nt find in the database."
                        }

                return redirect(f'/?message={context["message"]}')
        
        else:
            context = {
                        "response": 401,
                        "message": 'Invalid data.'
                    }

            return redirect(f'/?message={context["message"]}')

    context = {
                "response": 401,
                "message": f"Invalid http method, don't use {request.method}"
            }

    return redirect(f'/?message={context["message"]}')

@method_decorator(csrf_exempt)
def api_validate_token(request):

    if request.method == 'POST':
        form = forms.TokenForm(request.POST)

        if form.is_valid():

            jwt = JwtAuth()

            validation = jwt.validate_token(form.cleaned_data['token'])

            return HttpResponse (
                json.dumps (
                    validation
                )
            )
        
        else:
            return HttpResponse (
                json.dumps (
                    {
                        'response': 401,
                        'message': 'bad request, invalid data.'
                    }
                )
            )
    
    return HttpResponse (
                json.dumps (
                    {
                        'response': 401,
                        "message": f"Invalid http method, don't use {request.method}"
                    }
                )
            )

def api_logoff(request):
    if request.method != 'GET':
        return HttpResponse (
            json.dumps (
                {
                    'response': 401,
                    'message': f"Invalid http method, don't use {request.method}"
                }
            )
        )
    
    request.session['user_token'] = ''

    return redirect('/')


@method_decorator(csrf_exempt)
def create_contact(request):
    if request.method == 'POST':

        pass