# coding=utf-8
# Create your views here.

from datetime import datetime, timedelta
from django.http import  Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import urllib2
import thread  
from django.utils import timezone

from models import CampusTalk, CampusTalkInfo
from xjhSpider import beijingyoudiandaxue, qinghuadaxue, beihang, beijingdaxue, beijingligong, beijingkeji
from xjhSpider import shanghaijiaotongdaxue, tongjidaxue, fudandaxue, shanghaidaxue, donghuadaxue
from xjhSpider import huananligongdaxue, guangzhoudaxue, guangzhougongyedaxue, jinandaxue, zhongshandaxue


def bootstrap(request):
    return render_to_response("bootstrap.html")

def loadxjh(request):
#     response = urllib2.urlopen('http://www.baidu.com')
#     html = response.read()
    html = 'success'
    beijingyoudiandaxue()
    thread.start_new_thread(qinghuadaxue(),())
    beihang()
    beijingligong()
    thread.start_new_thread(beijingdaxue(),())
    response=HttpResponse()  
    response.write(html)  
    return response

def loadshxjh(request):
    html = 'success'
    shanghaijiaotongdaxue()
    tongjidaxue()
    fudandaxue()
    shanghaidaxue()
    donghuadaxue()
    response=HttpResponse()  
    response.write(html)  
    return response

def loadgzxjh(request):
    html = 'success'
    zhongshandaxue()
    huananligongdaxue()
    guangzhoudaxue()
    guangzhougongyedaxue()
    jinandaxue()
    thread.start_new_thread(beijingkeji(),())

    response=HttpResponse()  
    response.write(html)  
    return response

def loadurls(request):
    pass

def homepage(request):
    campustalk_list = CampusTalk.objects.all()
    return render_to_response("homepage.html",{"campustalk_list":campustalk_list},context_instance=RequestContext(request))

def campus_talk(request):
    campustalk_list = CampusTalk.objects.all()
    return render_to_response("campustalk_list.html",{"campustalk_list":campustalk_list},context_instance=RequestContext(request))


def campus_talk_info_list(request,univ_name):
    start_date = timezone.now().date()
    end_date = start_date + timedelta( days=100 )
#     if not page_index:
#         page_index = 1
#     else:
#         try:
#             page_index = int(page_index)  #传入的index参数是一个string，所以还是要先转成int
#         except ValueError:
#             raise Http404()
    
#     step = 10
    campustalk_info_list = CampusTalkInfo.objects.filter(campus_talk_date__range=(start_date, end_date), university_name_en__icontains = univ_name).order_by('campus_talk_date')
    length = len(campustalk_info_list)
#     page_num = int(length/step)
#     
#     if page_index*step+step > length:
#         m = length - page_index*step
#     else:
#         m =step
#     campustalk_info_list = campustalk_info_list[page_index*step:page_index*step+m]
    return render_to_response("campustalk_info_list.html",{"campustalk_info_list":campustalk_info_list,"univ_name":univ_name},context_instance=RequestContext(request))

def campus_talk_info_detail(request, index):
    try:
        index = int(index)  #传入的index参数是一个string，所以还是要先转成int
    except ValueError:
        raise Http404()
    campustalk_info_list = CampusTalkInfo.objects.filter(id=index) #这里返回的还是一个list，不是object
    return render_to_response("campustalk_info_detail.html",{"campustalk_info_list":campustalk_info_list},context_instance=RequestContext(request))    #给template传过去的是一个list


def campus_talk_detail(request, index):
    try:
        index = int(index)  #传入的index参数是一个string，所以还是要先转成int
    except ValueError:
        raise Http404()
    campustalk_list = CampusTalk.objects.filter(id=index) #这里返回的还是一个list，不是object
    return render_to_response("campus_talk_detail.html",{"campustalk_list":campustalk_list},context_instance=RequestContext(request))    #给template传过去的是一个list



def users_login(request):
    return render_to_response("users/login.html")

def users_signup(request):
    return render_to_response("users/signup.html")