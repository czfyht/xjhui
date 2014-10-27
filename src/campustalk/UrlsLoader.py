# -*- coding: utf-8 -*- 
from string import join
import urllib2  

from bs4 import BeautifulSoup

from campustalk.models import CampusTalkInfo
import sys
sys.setrecursionlimit(100000) #这里设置10万的递归深度

def qinghuaUrls():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="清华大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+1):
        url = 'http://xjh.haitou.cc/bj/uni-10/after/hold/page-'+ str(page_index) +'/'
        response = opener.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        tbody = soup.find(class_="preach-tbody")
        print tbody.find_all(class_="preach-tbody-title")[0].find("company").string
        
        
        