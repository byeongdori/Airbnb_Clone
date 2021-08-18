from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")

# 로그아웃 상태에서만 볼수 있는 mixins!
class LoggedOutOnlyView(UserPassesTestMixin):

    # permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 로그인 상태에서만 볼수 있는 mixins!
class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")

    def test_func(self):
        pass
