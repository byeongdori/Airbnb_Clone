from django.db import models
from core import models as core_models

# Create your models here.
class List(core_models.AbstractTimeStampedModel):

    """List Model Definition"""

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", related_name="lists", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()
    # short_description 사용하면 admin 페널에서 보이는 이름 변경 가능
    count_rooms.short_description = "Number of Rooms"