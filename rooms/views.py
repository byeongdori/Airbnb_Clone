from django.shortcuts import render
from . import models
# Create your views here.


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    # render 함수 - view에서 htmi 파일과 연결
    # contex 속성 - html 파일로 변수를 넘겨주고 싶을 때 사용
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms
        },
    )
