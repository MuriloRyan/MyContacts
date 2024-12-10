from django.shortcuts import render

# Create your views here.


def index(request):
    message = request.GET.get('message')
    log = False

    if 'user_token' in request.session:
        log = True if request.session['user_token'] != '' else False


    return render(request, "index.html", {'message': message, "login": log})

def register(request):
    return render(request, template_name="register.html")

def login(request):
    return render(request, template_name='login.html')