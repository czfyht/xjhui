from django.contrib import admin
from models import CampusTalk
from django.db import models
# class AuthorAdmin(admin.ModelAdmin):
# #     formfield_overrides = {
# #         models.TextField: {"widget": TinyMCE },
# #     }
#     class Media:
#         js=('http://127.0.0.1:8000/static/js/tinymce/js/tinymce/tinymce.min.js','http://127.0.0.1:8000/static/js')
     
admin.site.register(CampusTalk)
