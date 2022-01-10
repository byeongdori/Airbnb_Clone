from enum import Flag
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from requests.models import ReadTimeoutError
from core import models as core_models
from cal import Calendar, calendar

# Create your models here.


class AbstarctItem(core_models.AbstractTimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstarctItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstarctItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Ameities"


class Facility(AbstarctItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstarctItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.AbstractTimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.AbstractTimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # ForeignKey 이용하여 User model 과 연결, 일대다 관계
    # on_delete=models.CASCADE -> room 과 연결된 User가 삭제되면, room도 같이 삭제해라
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        # str 함수 -> 페이지에서 models가 보여지는 이름 설정
        return self.name

    # 이 save 메소드는 어드민에서 모델 건드릴 때 뿐만 아니라, 어딘가에서 건드릴 때 항상 일어남!
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    # Url 추적해주는 함수
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            # 사진이 없는 경우
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]
