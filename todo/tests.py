from django.contrib.auth.models import User
from django.test import TestCase

from todo.models import Task


class TaskModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user("ronan", password="pw")
        task = Task.create(user, "Test Title", "Test Desc")
        task.save()
        self.test_task_id = task.id

    def test_task_defaults(self):
        """
        Make sure we're getting expected defaults for values we don't specify
        during creation.
        """
        task = Task.objects.get(id=self.test_task_id)
        self.assertTrue(task.task_open)
        self.assertIsNone(task.marked_complete_by)
        self.assertIsNone(task.completed_date)

    def test_task_initial_data(self):
        task = Task.objects.get(id=self.test_task_id)
        owner = User.objects.get(username="ronan")
        self.assertEqual(owner, task.owner)
        self.assertEqual("Test Title", task.title)
        self.assertEqual("Test Desc", task.description)

    def test_complete_task(self):
        task = Task.objects.get(id=self.test_task_id)
        completer = User.objects.get(username="ronan")
        task.complete(completer)
        self.assertFalse(task.task_open)
        self.assertEqual(completer, task.marked_complete_by)
        self.assertIsNotNone(task.completed_date)

    def test_task_str(self):
        task = Task.objects.get(id=self.test_task_id)
        self.assertEqual("Test Title", str(task))


class TaskViewTest(TestCase):

    def setUp(self):
        pass

class TodoViewTest(TestCase):
    pass
