from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('campustalk.views',
    # Examples:
    # url(r'^$', 'campus.views.home', name='home'),
    # url(r'^campus/', include('campus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bootstrap/', 'bootstrap'),
    url('^$', 'homepage'),
    url(r'^users/login/', 'users_login'),
    url(r'^campustalk/detail/(\d+)/$', 'campus_talk_detail'),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
)
