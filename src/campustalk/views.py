# coding=utf-8
# Create your views here.

from django.http import  Http404
from django.shortcuts import render_to_response

from models import CampusTalk


def bootstrap(request):
    return render_to_response("bootstrap.html")

def homepage(request):
    campustalk_list = CampusTalk.objects.all()
    return render_to_response("homepage.html",{"campustalk_list":campustalk_list})

def campus_talk_detail(request, index):
    try:
        index = int(index)  #传入的index参数是一个string，所以还是要先转成int
    except ValueError:
        raise Http404()
    campustalk_list = CampusTalk.objects.filter(id=index) #这里返回的还是一个list，不是object
    return render_to_response("campus_talk_detail.html",{"campustalk_list":campustalk_list})    #给template传过去的是一个list
    
def users_login(request):
    return render_to_response("users/login.html")

def users_signup(request):
    return render_to_response("users/signup.html")