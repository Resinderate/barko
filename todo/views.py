from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods

from .models import Task


def todo(request):
	if request.user.is_authenticated():
		tasks = Task.objects.all()
		context = {}
		context.update(csrf(request))
		context["tasks"] = tasks
		return render_to_response("todo.html", context)
	else:
		return redirect("login")


@require_http_methods(["POST"])
def task(request):
	# Can't make a task if we don't have a user to own it.
	if not request.user:
		# Maybe return 400 instead.
		redirect("todo")

	user = request.user
	title = request.POST.get('title', '')
	description = request.POST.get('description', '')

	__create_new_task(user, title, description)

	return redirect("todo")

def __create_new_task(user, title, description):
	new_task = Task.create(user, title, description)
	new_task.save()
