from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.views import View

from todo.models import Task


class TodoView(View):
    def get(self, request):
        if request.user.is_authenticated():
            context = csrf(request)

            user = request.user
            context["user"] = user

            data = self._get_todo_data(user)
            context["task_lists"] = data

            return render_to_response("todo.html", context)
        else:
            return redirect("login")

    def _get_todo_data(self, current_user):
        current_user.is_current_user = True

        data = []
        
        users = User.objects.exclude(id=current_user.id)
        non_user_data = self._get_non_user_tasks(users)
        non_user_data = self._sort_users_on_task_count(non_user_data)

        current_user_tasks = self._get_user_tasks(current_user)
        
        data.append({"user": current_user, "tasks": current_user_tasks})
        data.extend(non_user_data)

        return data

    def _get_non_user_tasks(self, users):
        non_current_user_data = []
        for user in users:
            user_tasks = Task.objects.filter(
                owner=user
            ).order_by(
                "created_date"
            ).order_by(
                "-task_open"
            )
            for task in user_tasks:
                self._mark_filled_in_task_properties(task)
            non_current_user_data.append({"user": user, "tasks": user_tasks})
        return non_current_user_data

    def _sort_users_on_task_count(self, data):
        """
        :Params:
            data : List<dict>
                The dictionary must contain a 'tasks' key which contains list.
        """
        data.sort(key=lambda d: len(d["tasks"]), reverse=True)
        return data


    def _get_user_tasks(self, current_user):
        current_user_tasks = Task.objects.filter(
            owner=current_user
        ).order_by(
            "created_date"
        ).order_by(
            "-task_open"
        )
        for task in current_user_tasks:
            self._mark_filled_in_task_properties(task)
            task.is_current_user = True
        return current_user_tasks

    def _mark_filled_in_task_properties(self, task):
        properties = []
        # Values that will always be present
        properties.append({"header": "Description:",
                           "value": task.description or "None"})
        properties.append({"header": "Created at:", "value": task.created_date})
        properties.append({"header": "Completed:",
                           "value": self._get_task_complete_desc(task)})
        # Value that might be present
        # Completed by
        if task.marked_complete_by:
            properties.append({"header": "Completed By:",
                               "value": task.marked_complete_by.username})
        if task.completed_date:
            properties.append({"header": "Completed at:",
                               "value": task.completed_date})

        task.filled_in_properties = properties

    def _get_task_complete_desc(self, task):
        if task.task_open:
            return "No"
        else:
            return "Yes"


class TaskView(View):
    def post(self, request):
        """
        We can't create PUT or DELETE requests from a HTML form, so we're
        funneling them through the POST verb and then re-routing.
        """
        # Must be logged in to affect tasks.
        if not request.user:
            redirect("todo")

        # _method contains the true verb the form want to use, if it's not POST.
        method = request.POST.get("_method", "")
        if not method:
            return self._create_task(request)
        elif method == "PUT":
            completed = request.POST.get("completed", "")
            title = request.POST.get("title", "")
            description = request.POST.get("description", "")
            if completed and not (title or description):
                return self._complete_task(request)
            else:
                return self._edit_task(request)
        elif method == "DELETE":
            return self._delete_task(request)

        return self._no_valid_action()

    def _create_task(self, request):
        user = request.user
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        new_task = Task.create(user, title, description)
        new_task.save()

        return redirect("todo")

    def _complete_task(self, request):
        # Try get all the relavent data.
        user = request.user
        task_id = int(request.POST.get("task_id", ""))

        task = Task.objects.get(id=task_id)
        task.complete(user)

        return redirect("todo")

    def _edit_task(self, request):
        completed = request.POST.get("completed", "")
        task_open = self._parse_task_open_option(completed)
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        task_id = int(request.POST.get("task_id", ""))

        task = Task.objects.get(id=task_id)
        if task_open != task.task_open:
            self._toggle_complete(task, task_open, request.user)

        if title and title != task.title:
            task.title = title
            task.save()

        if description and description != task.description:
            task.description = description
            task.save()

        return redirect("todo")

    def _parse_task_open_option(self, value):
        """
        Inversing the result here. Switching from the UI verb 'complete' to
        model 'is_open'.
        """
        if value == "true":
            return False
        elif value == "false":
            return True
        else:
            return None

    def _toggle_complete(self, task, task_open, user):
        if task_open:
            task.uncomplete()
        else:
            task.complete(user)

    def _delete_task(self, request):
        task_id = int(request.POST.get("task_id", ""))
        task = Task.objects.get(id=task_id)
        if task.owner != request.user:
            return redirect("todo")

        task.delete()
        return redirect("todo")

    def _no_valid_task(self):
        redirect("todo")
