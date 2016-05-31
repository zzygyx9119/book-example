import sys
from accounts.models import Token
from django.contrib import auth
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages


def send_login_email(request):
    print('login view', file=sys.stderr)
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri('/accounts/login/{token}/'.format(token=token.uid))
    send_mail(
        'Your login link for Superlists',
        'Use this link to log into the site:\n\n {url}\n'.format(url=url),
        'noreply@superlists',
        [email],
    )
    messages.success(request, 'Check your email for a link to use to log in')
    return redirect('/')


def login(request, uid):
    user = auth.authenticate(uid=uid)
    if user is None:
        return render(request, 'login.html')
    auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
