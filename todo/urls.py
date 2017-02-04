from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.todo, name="todo"),
	url(r"^task/$", views.TaskView.as_view(), name="task")
]
