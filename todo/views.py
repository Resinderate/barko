from django.http import HttpResponse
from django.shortcuts import render_to_response

def todo(request):
	return render_to_response("login.html")
