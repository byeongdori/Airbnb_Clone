from django.core import paginator
from django.db.models.base import ModelState
from django.urls.base import reverse, reverse_lazy
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator
from django_countries import countries
from users import mixins as user_mixins
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
    paginate_by = 12

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


class RoomDetailView(DetailView):

    """Room Detail Definition"""

    model = models.Room

    # url에서 pk를 찾고자 할 때 키워드
    # 기본적으로 pk로 설정되어 있음, 바꾸고 싶을 때 변경
    pk_url_kwarg = "pk"


# 장고 form API을 이용해 만든 방법
class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        city = request.GET.get("city")

        if country:
            # 이미 한번 폼을 로드 한 경우
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("super_host")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                # 외래 키 참조하여 검색기능 생성!
                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price_lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms_gte"] = bedrooms

                if beds is not None:
                    filter_args["beds"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                # 다대다 관계 검색 필터
                for amenity in amenities:
                    filter_args["amenities"] = int(amenity)

                for facility in facilities:
                    filter_args["facilities"] = int(facility)

                queryset = models.Room.objects.filter(**filter_args).order_by("created")

                paginator = Paginator(queryset, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            # 초기 상태의 폼
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


# Django Form 사용 안하고 만든 방법
"""
def search(request):
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
    # get_page() -> 페이지 수가 음수&초과이면 마지막 페이지 반환 -> 유연성
    # page() -> 페이지 수가 음수&초과이면 오류 발생시킴 -> 예외 처리에 유용
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room

    template_name = "rooms/room_edit.html"

    # 뭘 수정할 것인지 필드 설정
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, RoomDetailView):

    model = models.Room

    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that Photo")
        else:
            # 사진 삭제
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))

class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        # DB에 object를 저장한 후에 many to many 필드 저장해줘야함!
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))