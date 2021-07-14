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

1. admin.py 에서 사용할 수 있는 기능들
 - fieldsets
 - list_display
 - list_filter
 - ordering
 - search_fields
   - 검색 방법은 prefix를 사용해 ^, =, @, None 네가지 방법으로 사용 가능
   - ^ -> StartsWith // = -> iexact // @ -> search // None -> icontains
   - ex) "=city" -> 정확한 도시 이름을 검색했을 때만 검색 결과 출력
 - filter_horizontal
   - filter_horizontal -> ManytoMany 관계에서 사용가능
   - 특정 model 생성 시, model 내의 여러개의 다른 요소 추가 / 제거 시 유용 

2. Managers and QuerySets
 - python manage.py shell 명령 통해 장고 DB 객체들에 접근할수 있음
 - 이때 접근하는 연결 다리가 Manager, 결과가 Queryset
 - Queryset -> Object 리스트 (데이터베이스로 부터 온 장고 리스트)