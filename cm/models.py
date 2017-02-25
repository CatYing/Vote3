# coding=utf8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=16)
    permission = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class Member(models.Model):
    name = models.CharField(max_length=256)
    sex = models.BooleanField()
    student_num = models.CharField(max_length=32)
    introduction = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d', null=True)

    class META:
        ordering = ['student_num']

    def __unicode__(self):
        return self.name


class Record(models.Model):
    member = models.ForeignKey(Member)
    voter = models.ForeignKey(MyUser)
    grade = models.CharField(max_length=16)

    def __unicode__(self):
        return self.voter.name + u"对" + self.member.name + str(self.grade)

