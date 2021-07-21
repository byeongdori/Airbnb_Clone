from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", {"rooms": rooms})

    # 아래는 paginator 사용하지 않고 쓴 코드
    """ 
    page = request.GET.get("page")
    # page에 값이 없으면 1로 넣겠다(Default 설정)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    # Room 객체를 [offset:limit] offset번째부터 limit번째까지 보고싶다
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    
    # render 함수 - view에서 htmi 파일과 연결
    # contex 속성 - html 파일로 변수를 넘겨주고 싶을 때 사용
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
    """
