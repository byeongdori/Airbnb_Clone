# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more..

Start 2021.07.04

0.

- app 생성시 config -> settings.py 가서 app 등록
  - -> INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS
    - --> DJANGO_APPS : 기본 제공
    - --> PROJECT_APPS : 개발하면서 만드는 app
    - --> THIRD_PARTY_APPS : 외부에서 가져온 app, 라이브러리
- models.py 변경시 makemigration -> migrate
- app -> 웹 사이트 설계 시 웹 프로그램이 해야할 일을 적당한 크기로 모듈화 한 것
- 개발 시 어떤 app을 만들건지, app의 역할이 정확히 뭔지, app내의 models의 속성은 무엇이
  필요한지 명확히 확인해야함

## models.py

1. Create/Modify Custom Model

- Models.py -> 장고 데이터베이스에 들어갈 models 속성 정의
- admin.py -> Models.py 바탕으로 사용자에게 보여질 admin 패널 관리

2. core apps

- 다른 app들이 공통적으로 사용하는 models의 속성을 추상적으로 정의
- 다른 app들이 상속받아 확장해서 사용
- Meta class 이용해 추상클래스로 설정

3. 일대다, 다대다 관계

- 일대다 관계 -> models.ForeignKey 함수 사용
- 다대다 관계 -> models.ManyToManyField 함수 사용

4. Meta class

- abstract = True -> 추상클래스 설정 가능 (ex. Core app)
- admin 패널에서 보이는 models 객체 관리 (ex. Ordering / 단수&복수형..)
- verbose_name / verbose_name_plural (영단어 단수&복수형)
- ordering (정렬 기능)

## admin.py

0. admin에게만 필요한 기능 -> admin.py에 함수 추가
   실 사용자에게도 보여지는 기능 -> models.py에 함수 추가

1. admin.py 에서 사용할 수 있는 기능들

- fieldsets
- list_display
  - models.py 에서 만든 함수를 요소로 집어넣을 수도 있음
- list_filter
- ordering
- raw_id_fields
  - 리스트에 선택지가 다수일 때, 특정 id로 검색해 선택하는 방법 제공
- search_fields
  - 검색 방법은 prefix를 사용해 ^, =, @, None 네가지 방법으로 사용 가능
  - ^ -> StartsWith // = -> iexact // @ -> search // None -> icontains
  - ex) "=city" -> 정확한 도시 이름을 검색했을 때만 검색 결과 출력
- filter_horizontal
  - filter_horizontal -> ManytoMany 관계에서 사용가능
  - 특정 model 생성 시, model 내의 여러개의 다른 요소 추가 / 제거 시 유용

2. Inline admin

- 한 admin.py 안에 다른 app의 admin을 넣을 때 사용
- 먼저 넣어야할 model의 Inline 클래스를 만들고, (ex. PhotoInline)  
  목적지 admin.py에 inline 변수 생성 후 할당 (ex. inline = (PhotoInline, ))
- admin 페이지에서 볼 땐 TabularInline / StackedInline 두 가지 형식 사용가능
- rooms -> admin.py에 예시 있음

3. Managers and QuerySets

- python manage.py shell 명령 통해 장고 DB 객체들에 접근할수 있음
- 파이썬 코드로도 접근 가능, 다른 models 참조하는 기능 요구하는 함수 작성 시 유용하게 사용 (ex. rooms -> admin.py 에 있음)
- 접근하는 연결 다리가 Manager, 결과가 Queryset
- Queryset -> Object 리스트 (데이터베이스로 부터 온 장고 리스트)
- Queryset에 관한 장고 설명
  - https://docs.djangoproject.com/en/3.2/ref/models/querysets/
- related_name -> 대상을 위한 속성
  - ex) amenities에 related_name = "rooms" 설정 시
    amenities.room_sets.all() -> amenities.rooms.all()로 사용
  - migrate 작업 해줘야함!

4. 업로드 파일 관리

- MEDIA_ROOT -> 장고 프로젝트 파일 내에 미디어(사진, 영상..) 파일들이 어디에 저장될지 설정하는 변수
- 또한 models.py에서 models.ImageField() 함수에서 upload_to 매개변수 사용하여 더 세세하게 구분 가능  
  (ex. file = models.ImageField(upload_to="room_photos")) -> MEDIA_ROOT 설정 된 폴더 내에 room_photos 라는 하위 폴더 만들어 거기에 저장)
- MEDIA_URL -> 웹 상에서 미디어 파일들의 URL을 설정하는 변수  
  (ex. MEDIA_URL = "/media/"로 설정 후 uploads/room_photos/testimage.jpg 열면 -> -> /media/room_photos/temsimage.jpg로 열림
- 위에 있는 MEDIA 관련 두 변수 설정 후, urls.py에서 실제 파일&폴더의 위치와 파일 URL을 연결해야 웹에서 파일이 보임!
  - 이때 개발 단계 & 라이브 서버인지 구분해서 파일 보이는 방법 설정해야함

5. save() / delete() 함수와 super()

- model 저장 시, 장고 내에 있는 부모 클래스에서 save() 함수 호출하여 저장함
- super() 메소드 통해 장고 내에 있는 부모 클래스 참조하여 save() 함수 오버라이딩(Overriding) 가능
- save() -> model이 저장되는 모든 시점에 동작  
  admin_save() -> admin 패널에서 저장 시에만 동작, 누가 저장했는지 확인 가능

6. 사용자 지정 명령어 / Django_seed 활용해서 손 쉽게 테스트 데이터 넣기

- 사용자가 명령을 만들어 python manage.py <사용자 명령> 형식으로 사용 가능
- 많은 데이터를 한꺼번에 생성하는 명령 만드는데에 유용
  - 손쉽게 데이터를 만들기 위한 장고 시드 활용시  
    pipenv install django_seed / config -> setting.py 서드파티 앱 추가
  - django_seed 활용법 -> rooms app 내에 seed_rooms.py 파일 참고
- 사용자 지정 명령어는 어떤 app에서 필요한 명령어 인지 따라 django app 내에 구분  
  app내에 management 폴더 만들고 **init**.py와 commands 폴더 생성  
  commands 폴더 내에 **init**.py 와 명령어.py 파일 생성
- 명령어.py 내에는 Command 클래스 만들어 명령어 호출 시 동작 설정  
  (ex. room app 내에 seed_rooms.py -> 호출은 python manage.py seed_rooms)

## urls.py & views.py & Html(templates)

0. Url(주소) - View(뷰, 함수들) - Html(템플릿)식으로 연결

1. Url

- urls은 앱 별로 앱 폴더 내에 urls.py 만들어 정리하기 (Divide and Conquer)
- 최종적으로 config -> urls.py에 각 앱으로 가는 url 경로 모아두기
- urls.py 내에 urlpatterns 변수가 url 관리 -> url과 view 연결?
- 어떤 앱 내에서 쓰이는 기능을 표현하는 url인지 네이밍 잘 해서 정리

2. View

- request - Httpresponce
- render 함수 -> view와 html 이어주는 다리

3. Html 파일

- html 파일은 Templates 폴더 새로 생성해서 관리
  - html 파일은 최대한 작게 기능, 부분별로 나누기 (Divide and Conquer)
  - config -> settings.py 에 생성한 Templates 폴더 위치 알려줘야함!
- 공통적으로 쓰이는 구조가 있는 경우, 모든 템플릿의 기본이 되는 템플릿(부모 템플릿) 생성해서 자식 템플릿에서 확장 (ex. base.html)
- block - 자식 템플릿이 부모 템플릿에게 content 집어넣을수 있는 도구
- include - 한 템플릿 안에 다른 템플릿 집어넣을수 있는 도구
- template tag 사용해서 html 파일에서 논리적 연산 수행 가능
  - template tag 장고 설명 문서 -> https://docs.djangoproject.com/en/3.2/ref/templates/builtins/
- 장고 Paginator -> view.py와 html 파일 코딩을 더 쉽게 할 수 있도록 도와주는 객체  
  (ex. rooms -> view.py 와 template -> rooms -> home.html 참고)
