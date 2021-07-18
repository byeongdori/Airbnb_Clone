from django.core.management.base import BaseCommand
from rooms import models as room_models

class Command(BaseCommand):

    # 이 Command에 대한 설명
    help = "This command creates amenities"

    # 명령어에 매개변수가 필요할 때 아래 함수 사용
    """
    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many")
    """

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Heating",
            "Washer",
            "Wifi",
            "Indoor fireplace",
            "Iron",
            "Laptop friendly workspace",
            "Crib",
            "Self check-in",
            "Carbon monoxide detector",
            "Shampoo",
            "Air conditioning",
            "Dryer",
            "Breakfast",
            "Hangers",
            "Hair dryer",
            "TV",
            "High chair",
            "Smoke detector",
            "Private bathroom",
        ]
        for a in amenities:
            room_models.Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenities Created"))
        
