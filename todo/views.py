from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect

def todo(request):
	if request.user.is_authenticated():
		return render_to_response("login.html")
	else:
		return redirect("login")
