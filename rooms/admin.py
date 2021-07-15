from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, object):
        return object.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price")

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "country",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    search_fields = ["city", "host__username"]
    # 검색 방법은 prefix를 사용해 ^, =, @, None 네가지 방법으로 사용 가능
    # ^ -> StartsWith // = -> iexact // @ -> search // None -> icontains
    # ex) "=city" -> 정확한 도시 이름을 검색했을 때만 검색 결과 출력

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )
    # filter_horizontal -> ManytoMany 관계에서 사용가능
    # 특정 model 생성 시, model 내의 여러개의 다른 요소 추가 / 제거 시 유용

    def count_amenities(self, object):
        # self -> 현재 속한 클래스 (RoomAdmin)
        # object -> 현재 Row
        # list_display에 함수 이름을 추가하는 방식으로 사용 가능
        return object.amenities.count()

    def count_photos(self, object):
        return object.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    pass
