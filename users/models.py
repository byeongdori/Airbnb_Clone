import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelState
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string

# 장고 데이터베이스에 들어갈 model을 정의하는 파일 / 수정시 makemigration -> migrate 해야함!

# Create your models here.
class User(AbstractUser):  # AbstaractUser가 제공하는 속성 + 아래 속성 확장 (AbstarctUser import 해야함)

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "OTHER"),
    )

    LANGUAGE_ENGLISH = "EN"
    LANGUAGE_KOREAN = "KR"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRNECY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = (
        (CURRNECY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    first_name = models.CharField(
        ("first name"), max_length=30, blank=True, default="Unnamed User"
    )
    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)

    # 이메일 인증을 위한 필드들
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="")

    # 로그인 방법
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)
    
    # 이메일 인증 함수
    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})