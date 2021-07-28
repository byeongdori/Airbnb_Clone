from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_ 함수 -> 데이터 정리 -> clean_data 함수로 데이터 확인
    # email, password 유효성 검사 (서로 관련있기 때문에 하나의 검사함수로 묶음)
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                # clean_ 함수 썻다면 반드시 cleaned_data 리턴!
                return self.cleaned_data
            else:
                # add_error ->  어느 필드에서 온 에러인지 설정해서 출력
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
