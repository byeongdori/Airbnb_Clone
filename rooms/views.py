from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from . import models

# Create your views here.
    # Class Based View(ListView) 사용 - 최종적으로 쉽게 사용하는 코딩 방법

class HomeView(ListView):
    
    """ Home View Definition """

    # 단순 속성에 값을 대입하는 것만으로 페이지 설정 가능
    model = models.Room

    # 한 페이지에 몇개 보여줄꺼냐
    paginate_by = 10

    # 페이지 고아 설정
    paginate_orphans = 5

    # 정렬 방식
    ordering = "created"

    # 페이지 탐색 키워드 - /?page = 1 에서 page 부분 키워드 설정
    # page_kwarg = "Roompage"

    # Queryset object 이름 설정, default -> object_list
    context_object_name = "rooms"

    # 중요 함수!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context



"""
    # paginator - 중간 단계에서의 코딩(Function Based View)
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    # paginator 객체 사용
    # orphans -> 마지막에 5개 이하로 남으면, 그냥 전 페이지에 모두 보여줘!
    paginator = Paginator(room_list, 10, orphans=5)
    # get_page -> 페이지 수가 음수&초과이면 마지막 페이지 반환 -> 유연성
    # page -> 페이지 수가 음수&초과이면 오류 발생시킴 -> 예외 처리에 유용
    try:
        page = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": page})
    except EmptyPage:
        page = paginator.page(1)
        return redirect("/")


    # 아래는 paginator 사용하지 않고 쓴 코드 - 가장 기본적인 단계에서의 코딩
    
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
