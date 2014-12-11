from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from campustalk.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'campusttalkinfo', CampusTalkInfoViewSet)
admin.autodiscover()
urlpatterns = [
    # '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += patterns('campustalk.views',
    # Examples:
    # url(r'^$', 'campus.views.home', name='home'),
    # url(r'^campus/', include('campus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bootstrap/', 'bootstrap'),
    url('^$', 'homepage'),
    url(r'^users/login/$', 'users_login'),
    url(r'^campustalk/$', 'campus_talk'),
    url(r'^campustalk/detail/(\d+)/$', 'campus_talk_detail'),
    url(r'^campustalk/list/([a-z]*)/$', 'campus_talk_info_list'),
    url(r'^campustalk/list/detail/(\d+)/$', 'campus_talk_info_detail'),
    url(r'^loadxjh/$', 'loadxjh'),
    url(r'^loadshxjh/$', 'loadshxjh'),
    url(r'^loadgzxjh/$', 'loadgzxjh'),
    url(r'^loadurls/$', 'loadurls'),
    url(r'^get_ct_json/$', 'get_ct_json'),
#     url(r'^data/Zhaopinzhushou.apk/$', 'bigFileView'),
#     url(r'^loadxjh/$', 'load_campus_talk'),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
)

urlpatterns += patterns('records.views',
    (r'^android/addrecord/$','addrecord_android'),
    (r'^android/login/$',  'android_login'),
    (r'^android/logout/$', 'android_logout'),
    (r'^android/signup/$', 'android_signup'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()