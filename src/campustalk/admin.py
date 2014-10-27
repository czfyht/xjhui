from django.contrib import admin
from models import CampusTalk,CampusTalkInfo
from django.db import models
# class AuthorAdmin(admin.ModelAdmin):
# #     formfield_overrides = {
# #         models.TextField: {"widget": TinyMCE },
# #     }
#     class Media:
#         js=('http://127.0.0.1:8000/static/js/tinymce/js/tinymce/tinymce.min.js','http://127.0.0.1:8000/static/js')
     
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('university_name','campus_talk_name', 'campus_talk_date')
    search_fields = ('campus_talk_name',)
    list_filter = ('campus_talk_date','university_name')
    date_hierarchy = 'campus_talk_date'
#     fields = ('university_name',)
    
admin.site.register(CampusTalk)
admin.site.register(CampusTalkInfo, AuthorAdmin)