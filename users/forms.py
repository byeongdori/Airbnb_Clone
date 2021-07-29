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


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # clean 함수 호출된 시점 후에 있는 변수들은 아직 클린 안된 상태임!
    # ex) clean_password 호출 시, password_1 변수는 아직 참조 불가!
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password_1(self):
        password = self.cleaned_data.get("password")
        password_1 = self.cleaned_data.get("password_1")

        if password != password_1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password
    
    def save(self):
        print("save")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()