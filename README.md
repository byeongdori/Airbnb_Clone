# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more..

Start 2021.07.04

0. 
 - app 생성시 config -> settings.py 가서 app 등록
   -> INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS
    --> DJANGO_APPS : 기본 제공
    --> PROJECT_APPS : 개발하면서 만드는 app
    --> THIRD_PARTY_APPS : 외부에서 가져온 app, 라이브러리
 - models.py 변경시 makemigration -> migrate 

1. Create/Modify Custom User Model
 - Models.py -> 장고 데이터베이스에 들어갈 models 속성 정의
 - admin.py -> Models.py 바탕으로 사용자에게 보여질 admin 패널 관리

2. core apps 
 - 다른 app들이 공통적으로 사용하는 models을 추상적으로 정의
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