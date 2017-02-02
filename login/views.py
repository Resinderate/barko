from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
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
            return redirect("login")

    else:
        token = {}
        token.update(csrf(request))
        return render_to_response('auth/login.html', token)

def logout(request):
    auth.logout(request)
    return redirect("login")