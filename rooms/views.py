from django.shortcuts import render
from . import models
# Create your views here.


def all_rooms(request):
    page = int(request.GET.get("page", 1))
    # page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    # Room 객체를 [offset:limit] offset번째부터 limit번째까지 보고싶다
    all_rooms = models.Room.objects.all()[offset:limit]

    # render 함수 - view에서 htmi 파일과 연결
    # contex 속성 - html 파일로 변수를 넘겨주고 싶을 때 사용
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms
        },
    )
