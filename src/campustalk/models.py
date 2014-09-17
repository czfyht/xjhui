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
    
