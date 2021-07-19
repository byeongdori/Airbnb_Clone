import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    # 이 Command에 대한 설명
    help = "This command creates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many rooms do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        # foreign key인 속성 & random & 범위가 필요한 속성들은 lambda 함수 사용
        # 사용 안해도 기본적으로 속성 찾아서 형식에 맞게 랜덤한 데이터 넣어주기는 함
        seeder.add_entity(
            room_models.Room,
            number,
            {
                # seeder.faker -> 임의로 주소, 이름 등등 생성해줌
                "name": lambda x: seeder.faker.address(),
                # 일대 다 관계에서의 데이터 넣는 방법, choice 함수 사용
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(0, 20),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )
        created_rooms = seeder.execute()
        # flatten -> seeder.execute한 room 객체의 id를 list로 정리?해줌
        # 그냥 list에 넣어버리면 2중 배열이 되어버림
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            # Photo 객체 생성
            for i in range(1, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1, 31)}.webp",
                )
            # 다대다 관계에서의 데이터 넣는 방법
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for h in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(h)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created"))
