from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.shortcuts import redirect


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("todo")
        else:
            # Return errors to login.
            # Maybe just an single generic login.
            return redirect("login")

    else:
        token = {}
        token.update(csrf(request))
        return render_to_response("auth/login.html", token)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username, password=password)
        return redirect("login")
    else:
        token = {}
        token.update(csrf(request))
        return render_to_response("auth/register.html", token)

def logout(request):
    auth.logout(request)
    return redirect("login")