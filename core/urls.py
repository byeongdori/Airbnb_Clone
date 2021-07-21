from django.urls import path
from rooms import views as room_views

# app_name -> config에 있는 urls.py 에서 namespace가 참조하기 위한 이름 저장한 변수
app_name = "core"

urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home"),
]
