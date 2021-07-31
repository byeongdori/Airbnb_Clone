from users import models
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms

# Create your views here.

# FormView 사용하여 만드는 방법
class LoginView(FormView):

    template_name = "users/login.html"

    form_class = forms.LoginForm

    # reverse_lazy -> view는 로드 됐으나, url이 아직 로드되지 않을 때 사용
    success_url = reverse_lazy("core:home")

    initial = {"email": "initial@initial.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SingUpView(FormView):

    template_name = "users/signup.html"

    form_class = forms.SignUpForm

    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "Kim",
        "last_name": "ByeongJu",
        "email": "test@test.com",
    }

    # 회원가입이 됐다면 바로 로그인을 시킴
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

# 이메일 인증
def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# 단순 View 상속받아 만든 로그인 방법
"""
class LoginView(View):

    def get(self, request):
        form = forms.LoginForm(initial={"email": "initial@email.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # 로그인 과정! (Form에서 데이터 검사가 선행되어야 함)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # 로그인 인증 함수
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # 로그인 성공시 이동하는 화면
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
"""
