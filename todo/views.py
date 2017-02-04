from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views import View
from django.views.decorators.http import require_http_methods

from .models import Task


def todo(request):
    if request.user.is_authenticated():
        task_map = get_todo_data()

        context = {}
        context.update(csrf(request))
        context["task_map"] = task_map

        return render_to_response("todo.html", context)
    else:
        return redirect("login")

def get_todo_data():
    users = User.objects.all()
    # Might need a list so you can sort by number of tasks.
    task_map = {}

    for user in users:
        user_tasks = Task.objects.filter(owner=user)
        task_map[user] = user_tasks

    return task_map


def sort_by_most_tasks():
    pass


# Get rid of this.
@require_http_methods(["POST"])
def task(request):


class TaskView(View):
    def post(self, request):
        # Can't make a task if we don't have a user to own it.
        if not request.user:
            # Maybe return 400 instead.
            redirect("todo")

        user = request.user
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')

        __create_new_task(user, title, description)

        return redirect("todo")

    def put(self, request):
        # Need some logic to handle if we're updating anything.

        # Try get all the relavent data.
        user = request.user
        title = request.POST.get('title', '')

        # Based on this, can see if it's a "Edit Task" or a "Complete"
        # Do whichever it is
        pass

    def delete(self, request):
        # Check the permissions.
        # Delete the record.
        pass

    def __create_new_task(user, title, description):
        new_task = Task.create(user, title, description)
        new_task.save()
