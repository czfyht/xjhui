from django.contrib import admin
from records.models import UserProfile,Record

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user','companyname_cn', 'post')
    search_fields = ('user__nick_name',)
    
#     fields = ('user',)

admin.site.register(UserProfile)
admin.site.register(Record, AuthorAdmin)