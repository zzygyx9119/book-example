import sys
from accounts.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.core.mail import send_mail


def send_login_email(request):
    print('login view', file=sys.stderr)
    email = request.POST['email']
    token = Token.objects.create(email=email)
    send_mail(
        'Your login code for superlists',
        'Use this code to log into the site:\n\n {uid}\n'.format(uid=token.uid),
        'noreply@superlists',
        [email],
    )
    return redirect('login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            token = Token.objects.create(email=email)
            send_mail(
                'Your login code for superlists',
                'Use this code to log in:\n\n {uid}\n'.format(uid=token.uid),
                'noreply@superlists',
                [email],
            )
            return redirect('login')

def foo():

    user = authenticate(uid=request.POST['uid'].strip())
    if user is None:
        return render(request, 'login.html')
    auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
