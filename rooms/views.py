from django.db.models.base import ModelState
from django.urls.base import reverse
from django.http import Http404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from django_countries import countries
from . import models
from . import forms

# Create your views here.
# Class Based View(ListView) 사용 - 최종적으로 쉽게 사용하는 코딩 방법

# Class Based View
class HomeView(ListView):

    """Home View Definition"""

    # 단순 속성에 값을 대입하는 것만으로 페이지 설정 가능
    # html 파일에서 room 혹은 object라는 이름으로 받아온 model 참조 가능
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


class RoomDetail(DetailView):

    """Room Detail Definition"""

    model = models.Room

    # url에서 pk를 찾고자 할 때 키워드
    # 기본적으로 pk로 설정되어 있음, 바꾸고 싶을 때 변경
    pk_url_kwarg = "pk"


def search(request):

    # Django Form 사용
    form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})

    # Django Form 사용 안하고 만든 방법
    """
    city = request.GET.get("city") or "Anywhere"
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    super_host = bool(request.GET.get("super_host", False))
    # 여러개를 선택한 걸 가져올 땐 getlist!
    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "selected_room_type": room_type,
        "selected_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # 검색 기능 
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    # 외래 키 참조하여 검색기능 생성!
    if room_type != 0:
        filter_args["room_type__pk"] = room_type
    
    if price != 0:
        filter_args["price_lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests
    
    if bedrooms != 0:
        filter_args["bedrooms_gte"] = bedrooms
    
    if beds != 0:
        filter_args["beds"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths
    
    if instant is True:
        filter_args["instant_book"] = True
    
    if super_host is True:
        filter_args["host__superhost"] = True

    # 다대다 관계 검색 필터
    if len(selected_amenities) > 0:
        for s_amenity in selected_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(selected_facilities) > 0:
        for s_facility in selected_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms" : rooms},
    )
    """


# Function Based View
"""
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", {"room": room})
    except models.Room.DoesNotExist:
        # reverse 함수 -> urls.py에서 정의한 url pattern의 name에 매칭되는 url로 돌아감!
        return redirect(reverse("core:home"))
        # 404 page를 띄워줄 수도 있음! , 404.html 만들어서 커스텀도 가능
        # raise Http404()
"""

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
