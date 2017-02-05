from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.views import View


class LoginView(View):
    def get(self, request):
        context = csrf(request)
        return render_to_response("auth/login.html", context)

    def post(self, request):
        form_data = self._get_login_data(request)
        user = auth.authenticate(
            username=form_data["username"],
            password=form_data["password"]
        )

        if user is not None:
            return self._login_user(request, user)
        else:
            return self._incorrect_login_error()
            

    def _get_login_data(self, request):
        data = {}
        data["username"] = request.POST.get("username", "")
        data["password"] = request.POST.get("password", "")
        return data

    def _login_user(self, request, user):
        auth.login(request, user)
        return redirect("todo")

    def _incorrect_login_error(self):
        context = {"error": "Incorrect username or password."}
        return render_to_response("auth/login.html", context)

class RegisterView(View):
    def get(self, request):
        context = csrf(request)
        return render_to_response("auth/register.html", context)

    def post(self, request):
        form_data = self._get_register_data(request)
        if self._passwords_are_same(form_data["password"],
                                    form_data["confirm_password"]):
            return self._register_user(form_data["username"], form_data["password"])
        else:
            return self._return_different_password_error()

    def _get_register_data(self, request):
        data = {}
        data["username"] = request.POST.get("username", "")
        data["password"] = request.POST.get("password", "")
        data["confirm_password"] = request.POST.get("confirm_password", "")
        return data
    
    def _passwords_are_same(self, password, repeated_password):
        return password == repeated_password

    def _return_different_password_error(self):
        context = csrf(request)
        context = {"error": "Passwords do not match."}
        return render_to_response("auth/register.html", context)

    def _register_user(self, username, password):
        user = User.objects.create_user(username, password=password)
        return redirect("login")
    
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect("login")
    