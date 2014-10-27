from DjangoUeditor.models import UEditorField
from django.db import models


# Create your models here.
class CampusTalk(models.Model):
    company_name = models.CharField(max_length=40)
    university = models.CharField(max_length=40)
    date = models.DateTimeField("YYYY-MM-DD HH:MM:ss", blank=True, null=True)
    location = models.CharField(max_length=60)
    author = models.CharField(max_length=20)
    content = UEditorField(u'content', width=600, height=300, toolbars="full", imagePath="", filePath="", upload_settings={"imageMaxSize":1204000},
             settings={}, command=None,  blank=True) 
    def __unicode__(self):
        return u'%s %s' % (self.company_name, self.university)

class CampusTalkInfo(models.Model):
    university_name = models.CharField(max_length=40)
    university_name_short = models.CharField(max_length=20)
    university_name_en = models.CharField(max_length=20)
    city_name = models.CharField(max_length=20)
    campus_talk_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=40)
    campus_talk_date = models.DateTimeField("YYYY-MM-DD HH:MM:ss", blank=True, null=True)
    campus_talk_location  = models.CharField(max_length=60)
    href_url = models.URLField(verify_exists = False)
    info_source = models.CharField(max_length=50)
    company_introduce = UEditorField(u'content', width=600, height=300, toolbars="full", imagePath="", filePath="", upload_settings={"imageMaxSize":1204000},
             settings={}, command=None,  blank=True) 
    def __unicode__(self):
        return u'%s %s %s' % (self.campus_talk_name, self.university_name, self.campus_talk_date)
    
class CampusTalkUrl(models.Model):
    university_name = models.CharField(max_length=40)
    campus_talk_name = models.CharField(max_length=50)
    href_url = models.URLField(verify_exists = False)
    def __unicode__(self):
        return u'%s %s' % (self.university_name, self.campus_talk_name, self.href_url)
