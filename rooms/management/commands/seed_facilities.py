from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    # 이 Command에 대한 설명
    help = "This command creates facilities"

    """
    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many")
    """

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            room_models.Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facilities Created"))
