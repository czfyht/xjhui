# -*- coding: utf-8 -*-
# Create your views here.
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404,HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext 

from django.contrib.sites.models import get_current_site
from django.utils import simplejson

from records.forms import ContactForm, UserProfileForm, RecordForm
from records.models import UserProfile, Record


def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date': now})

def hour_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


def search(request):
    errors = []
    if 'q' in  request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            userProfile = UserProfile.objects.filter(nick_name__icontains=q)
            return render_to_response('search_results.html',
            {'users': userProfile, 'query': q})
    return render_to_response('search_form.html', {'errors': errors
                                                   })
    
def contact(request):
    print request
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('noreply@qq.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))
#     return render_to_response('contact_form.html',
#         {'errors': errors},c)
#     return render_to_response('contact_form.html',
#         {'errors': errors,
#        'subject': request.POST.get('subject', ''),
#        'message': request.POST.get('message', ''),
#        'email': request.POST.get('email', ''),},
#       context_instance=RequestContext(request))
    
def contact_thanks(request):
    return render_to_response('contact_thanks.html')

@login_required  
def add_users(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            userProfile = UserProfile()
            userProfile.nick_name = cd['nick_name']
            userProfile.user = request.user
            userProfile.save()
#             UserProfile.objects.create(nick_name = cd['nick_name'])
            return HttpResponseRedirect('/addusers/thanks/')
    else:
        form = UserProfileForm()
    return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))

def add_users_thanks(request):
    return render_to_response('add_users_thanks.html')

@login_required 
def addrecord_android(request):
    if request.method == 'POST':
#         form = RecordForm(request.POST)
#         if form.is_valid():
            reqJson = simplejson.loads(request.raw_post_data)
            record = Record()
            record.user = request.user
            record.companyname_cn = reqJson['companyname_cn']
            record.city = reqJson['city']
            record.post = reqJson['post']
#             record.date = reqJson['date']
#             record.time = reqJson['time']
            record.date_time = reqJson['dateTime']
            record.location = reqJson['location']
            record.state = reqJson['state']
            record.orig_record_id = reqJson['orig_record_id']
#             record.post = reqJson['post']
            try:
                record.save()
                
            except Exception,e:
                print str(e)
                return HttpResponse(str(e))
            else:
                return HttpResponse("added")
#     return("added failed")
#     else:
#         form = RecordForm()
#     return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))
    

def adduser_android(request): 
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            UserProfile.objects.create(nick_name = cd['nick_name'])
            return HttpResponse("user added!",context_instance=RequestContext(request))
        else:
            return HttpResponse("failed",context_instance=RequestContext(request))
    return HttpResponse("set csrf",context_instance=RequestContext(request))
    
        
def android_login(request):
    template_name = 'users/android_login.html'
    redirect_field_name = 'next'
    redirect_to = '/accounts/profile'
    if request.user.is_authenticated():
            return HttpResponse('the user is logged in')
    else:
        
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # Correct password, and the user is marked "active"
                auth.login(request, form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                # Redirect to a success page.
#                 return HttpResponse('logged in successfully')
                return HttpResponse('login successfully')
            else:
                # Show an error page
                current_site = get_current_site(request)
                context = {
                    'form': form,
                    redirect_field_name: redirect_to,
                    'site': current_site,
                    'site_name': current_site.name,
                }
                return render_to_response(template_name, context,context_instance=RequestContext(request))
        else:
            form = AuthenticationForm(request)
            request.session.set_test_cookie()
    
        current_site = get_current_site(request)
    
        context = {
            'form': form,
            redirect_field_name: redirect_to,
            'site': current_site,
            'site_name': current_site.name,
        }
        return render_to_response(template_name, context,context_instance=RequestContext(request))

def android_logout(request):
    if request.method == 'POST' and request.user.is_authenticated():
        auth.logout(request)
        return HttpResponse('logout successfully')
#     if request.user.is_authenticated():
#         return HttpResponse('the user is logged in')
    return render_to_response('users/android_logout.html',context_instance=RequestContext(request))

def android_signup(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
#         authForm = AuthenticationForm(data=request.POST)
#         userForm = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()     #这一步可以保存这个form
#             auth.login(request, authForm.get_user())
            return HttpResponse('signup successfully')
#             if userForm.is_valid():
#                 cd = userForm.cleaned_data
#                 User.objects.create(user_name = cd['username'],nick_name = cd['nick_name'])
    else:
        form = UserCreationForm()
    return render_to_response("users/android_register.html", {
        'form': form,
    },context_instance=RequestContext(request))


