# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    user_name = models.CharField(max_length = 20)
    nick_name = models.CharField(max_length = 60)
    school = models.CharField(max_length = 60)
    college = models.CharField(max_length = 60)
    graduation_year = models.CharField(max_length = 20)
    def __unicode__(self):
        return u'%s %s' % (self.user_name,self.nick_name)

    
class Record(models.Model):
    user = models.ForeignKey(User)      #这个record对应的User
    orig_record_id = models.IntegerField()
    companyname_cn = models.CharField(max_length = 30, null=True)
    companyname_en = models.CharField(max_length = 40, null=True)
    city = models.CharField(max_length = 10, null=True)    #城市
    post = models.CharField(max_length = 20, null=True)    #岗位
    date_time = models.DateTimeField("YYYY-MM-DD HH:MM:ss",blank=True, null=True)   #日期+时间
    location = models.CharField(max_length = 60, null=True)    #地点
    state = models.CharField(max_length = 10, null=True)       #状态
    remark = models.CharField(max_length = 200, null=True)  #备注
    timestamp = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return u'%s %s' % (self.companyname_cn, self.post)
