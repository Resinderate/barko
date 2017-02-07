from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from todo.models import Task
from todo.views import TodoData


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("ronan", password="pw")
        self.task = Task.create(self.user, "Test Title", "Test Desc")

    def test_task_defaults(self):
        """
        Make sure we're getting expected defaults for values we don't specify
        during creation.
        """
        self.assertTrue(self.task.task_open)
        self.assertIsNone(self.task.marked_complete_by)
        self.assertIsNone(self.task.completed_date)

    def test_task_initial_data(self):
        self.assertEqual(self.user, self.task.owner)
        self.assertEqual("Test Title", self.task.title)
        self.assertEqual("Test Desc", self.task.description)

    def test_complete_task(self):
        self.task.complete(self.user)
        self.assertFalse(self.task.task_open)
        self.assertEqual(self.user, self.task.marked_complete_by)
        self.assertIsNotNone(self.task.completed_date)

    def test_task_str(self):
        self.assertEqual("Test Title", str(self.task))


class TaskViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("ronan", password="pw")

    def test_valid_create_task(self):
        self.client.login(username="ronan", password="pw")
        response = self.client.post(reverse("task"), follow=True)
        self.assertEqual(1, len(Task.objects.all()))
        self.assertRedirects(response, reverse("todo"))

    def test_edit_task_complete(self):
        self.client.login(username="ronan", password="pw")
        task = Task.create(self.user, "blah", "blah")
        response = self.client.post(reverse("task"),
                                    {"_method": "PUT",
                                     "task_id": 1,
                                     "completed": "true"},
                                    follow=True)
        task.refresh_from_db()
        self.assertFalse(task.task_open)
        self.assertRedirects(response, reverse("todo"))

    def test_edit_task_all(self):
        self.client.login(username="ronan", password="pw")
        task = Task.create(self.user, "blah", "blah")
        response = self.client.post(reverse("task"),
                                    {"_method": "PUT",
                                     "task_id": 1,
                                     "title": "new title",
                                     "description": "new desc",
                                     },
                                    follow=True)
        task.refresh_from_db()
        self.assertEqual("new title", task.title)
        self.assertEqual("new desc", task.description)
        self.assertRedirects(response, reverse("todo"))

    def test_delete_task(self):
        self.client.login(username="ronan", password="pw")
        task = Task.create(self.user, "blah", "blah")
        response = self.client.post(reverse("task"),
                                    {"_method": "DELETE",
                                     "task_id": 1,
                                     },
                                    follow=True)
        tasks = Task.objects.all()
        self.assertEqual(0, len(tasks))
        self.assertRedirects(response, reverse("todo"))

    def test_no_valid_action(self):
        self.client.login(username="ronan", password="pw")
        response = self.client.post(reverse("task"),
                                    {"_method": "FAKE"},
                                    follow=True)
        self.assertRedirects(response, reverse("todo"))

    def test_not_logged_in(self):
        response = self.client.post(reverse("task"), follow=True)
        self.assertRedirects(response, reverse("login"))

    def test_get_invalid_method(self):
        response = self.client.get(reverse("task"))
        self.assertEqual(405, response.status_code)


class TodoViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("ronan", password="pw")

    def test_valid_request(self):
        self.client.login(username="ronan", password="pw")
        response = self.client.get(reverse("todo"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "todo.html")

    def test_denies_anon(self):
        response = self.client.get(reverse("todo"), follow=True)
        self.assertRedirects(response, reverse("login"))


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
