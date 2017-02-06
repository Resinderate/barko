from django.contrib.auth.models import User
from django.test import TestCase

from todo.models import Task
from todo.views import TodoData


class TaskModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user("ronan", password="pw")
        task = Task.create(user, "Test Title", "Test Desc")
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
    pass



class TodoViewTest(TestCase):
    pass


class TodoDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ronan", password="pw")

    def test_no_tasks(self):
        """
        If there are no tasks at all we should still get the users empty list.
        """
        data = TodoData(self.user).data()
        self.assertEqual(1, len(data))
        self.assertEqual({"user": self.user, "tasks": []}, data[0])

    def test_users_sorted_by_number_of_tasks(self):
        user_little = User.objects.create_user("little", password="pw")
        user_lots = User.objects.create_user("lots", password="pw")

        Task.create(user_little, "title1", "desc1")
        Task.create(user_lots, "title2", "desc2")
        Task.create(user_lots, "title3", "desc3")

        data = TodoData(self.user).data()

        self.assertEqual(user_lots, data[1]["user"])
        self.assertEqual(user_little, data[2]["user"])

    def test_tasks_sorted_newest(self):
        older = Task.create(self.user, "older", "older desc")
        newer = Task.create(self.user, "newer", "newer desc")
        newest = Task.create(self.user, "newest", "newest desc")

        data = TodoData(self.user).data()

        self.assertEqual(older, data[0]["tasks"][0])
        self.assertEqual(newer, data[0]["tasks"][1])
        self.assertEqual(newest, data[0]["tasks"][2])

    def test_tasks_sorted_by_compelted(self):
        completed = Task.create(self.user, "completed", "completed desc")
        completed.complete(self.user)
        uncompleted = Task.create(self.user, "uncompleted", "uncompleted desc")

        data = TodoData(self.user).data()

        self.assertEqual(uncompleted, data[0]["tasks"][0])
        self.assertEqual(completed, data[0]["tasks"][1])

    def test_users_with_no_tasks_ignored(self):
        has_tasks = User.objects.create_user("hastasks", password="pw")
        no_tasks = User.objects.create_user("notasks", password="pw")

        user_task = Task.create(self.user, "user_task", "desc")
        has_tasks_task = Task.create(has_tasks, "has_tasks_task", "desc")

        data = TodoData(self.user).data()

        self.assertEqual(2, len(data))
        self.assertFalse({"user": no_tasks, "tasks": []} in data)

    def test_user_always_first(self):
        """
        User's list should always be first, even if they have 0 tasks and
        another user has 1+ tasks.
        """
        other_user = User.objects.create_user("other", password="pw")
        task = Task.create(self.user, "user_task", "desc")

        data = TodoData(self.user).data()
        self.assertEqual(self.user, data[0]["user"])
