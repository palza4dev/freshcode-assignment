from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    email    = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    role     = models.CharField(verbose_name='등급', max_length=10, choices=(('admin', '관리자'),('user', '사용자')))
    
    class Meta:
        db_table = 'users'