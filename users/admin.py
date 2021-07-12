from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.migrations.operations import models
from . import models

# 작업한 models.py를 직접적으로 웹에 보여지게 하는 파일

# Register your models here.
@admin.register(models.User)       # models.py에 있는 User Model 등록, 아래 Class 정의와 한쌍
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    # 한 속성들의 집합? 유저 정보창의 파란색으로 구분되는 집합
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    # 리스트 목록 보여줄 때 함께 보여줄 속성들 설정
    list_display = (
        "username",
        "gender",
        "language",
        "currency",
        "superhost",
    )
    # 리스트들을 특정 속성들로 필터링해서 보고 싶을 때 설정
    list_filter = (
        "language",
        "currency",
        "superhost",
    )
