from django.db import models

# Create your models here.
# User app을 제외한 다른 app들은 이 Core app을 확장하여 사용
class AbstractTimeStampedModel(models.Model):

    """Time Stamed Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add -> 생성 날짜 기록 // auto_now -> 업데이트 날짜 기록

    class Meta:
        abstract = True

    """ 데이터베이스에 등록하지 않기 위해 추상 클래스로 설정
        확장해서 사용하는 app들이 데이터베이스에 들어갈 것이기 때문"""
