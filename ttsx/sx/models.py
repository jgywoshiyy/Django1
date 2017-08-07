# coding=utf-8
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=40)


class RecPerson(models.Model):
    recname = models.CharField(max_length=20)
    recphonenumber = models.IntegerField
    recaddress = models.CharField(max_length=100)
    recpuser = models.ForeignKey('UserInfo')

