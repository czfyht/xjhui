# -*- coding: utf-8 -*- 
from string import join
import urllib2  

from bs4 import BeautifulSoup

from campustalk.models import CampusTalkInfo
import sys
sys.setrecursionlimit(100000) #这里设置10万的递归深度

#北京邮电大学
def beijingyoudiandaxue():
    url = 'http://job.bupt.edu.cn/career/careerTalkDetail'
    try:
#         file = open('beijingyoudian.html','r')
        opener=urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        response = opener.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        beiyou_list = CampusTalkInfo.objects.filter(university_name="北京邮电大学")
#         print type(beiyou_list)
        for tr in soup.tbody.find_all("tr"):
            td_list = tr.find_all("td")
            campusTalkInfo = CampusTalkInfo()
            campusTalkInfo.campus_talk_date = unicode(td_list[0].string)+' '+unicode(td_list[3].string[0:5])+':00'
            campusTalkInfo.campus_talk_date = join(campusTalkInfo.campus_talk_date.split())
            campusTalkInfo.href_url = td_list[1].a['href']
            campusTalkInfo.info_source = unicode(soup.title.string)
            campusTalkInfo.campus_talk_name = unicode(td_list[1].a.string).replace(u'2015校园招聘宣讲会',u'')
            campusTalkInfo.campus_talk_location = unicode(td_list[4].string)
            campusTalkInfo.company_name = unicode(td_list[2].string)
            campusTalkInfo.university_name = u'北京邮电大学'
            campusTalkInfo.university_name_short = u'北邮'
            campusTalkInfo.university_name_en = u'bupt-beijing'
            if beiyou_list:
                xjh = beiyou_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_='contentDiv clearfix')
                    campusTalkInfo.save()
            else:
#                 print 'list = null'
                detail_url = campusTalkInfo.href_url
                detail_opener=urllib2.build_opener()
                detail_opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                detail_response = detail_opener.open(detail_url)
                detail_html = detail_response.read()
                detail_soup = BeautifulSoup(detail_html)
                campusTalkInfo.company_introduce = detail_soup.find(class_='contentDiv clearfix')
                campusTalkInfo.save()
        return u'beiyou' 

    except Exception,e:  
        print str(e)
  
def beijingdaxue():
    beida_list = CampusTalkInfo.objects.filter(university_name="北京大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+2):
        try:
            url = 'http://xjh.haitou.cc/bj/uni-11/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'北京大学就业信息网'
                campusTalkInfo.university_name = u'北京大学'
                campusTalkInfo.university_name_short = u'北大'
                campusTalkInfo.university_name_en = u'pku-beijing'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = beida_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功' 
        
#清华大学        
# def qinghuadaxue():
#     url = 'http://xjh.yjbys.com/tsinghua/'
# 
#     try:
#         opener=urllib2.build_opener()
#         opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
#         response = opener.open(url)
#         html = response.read()
#         soup = BeautifulSoup(html)
#         qinghua_list = CampusTalkInfo.objects.filter(university_name="清华大学")
#         for tr in soup.table.find_all("tr"):
#             if tr.find("th"):
#                 continue
#             td_list = tr.find_all("td")
#             campusTalkInfo = CampusTalkInfo()
#             campusTalkInfo.campus_talk_name = unicode(td_list[3].find("a").string)
#             print campusTalkInfo.campus_talk_name
#             
#             end = td_list[2].string.find('-')
#             if end > 0:
#                 campusTalkInfo.campus_talk_date = unicode(td_list[1].string[0:10])+' '+unicode(td_list[2].string[0:end])
#             else:
#                 campusTalkInfo.campus_talk_date = unicode(td_list[1].string[0:10])+' 00:00'
#             campusTalkInfo.info_source = u'清华大学毕业生就业信息网'
#             campusTalkInfo.university_name = u'清华大学'
#             campusTalkInfo.university_name_short = u'清华'
#             campusTalkInfo.campus_talk_location = unicode(td_list[5].find("font").string)
#             campusTalkInfo.university_name_en = u'tsinghua-beijing'
#             campusTalkInfo.company_introduce = u'暂无宣讲会介绍'
#             if qinghua_list:
#                 xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
#                 if xjh:
#                     if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
#                         xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
#                         xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
#                         xjh[0].save()
#                 else:
#                     campusTalkInfo.save()
#             else:
#                 campusTalkInfo.save()
#         return u'Tsinghua'
#     except Exception,e:  
#         print str(e)

def qinghuadaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="清华大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+3):
        try:
            url = 'http://xjh.haitou.cc/bj/uni-10/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'清华大学毕业生就业信息网'
                campusTalkInfo.university_name = u'清华大学'
                campusTalkInfo.university_name_short = u'清华'
                campusTalkInfo.university_name_en = u'tsinghua-beijing'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)

                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])
                
                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功' 

        
        
def beihang():
    beihang_list = CampusTalkInfo.objects.filter(university_name_short="北航")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
 
    for page_index in range(1, 1+3):
        url = 'http://career.buaa.edu.cn/getJobfairAllInfoAction.dhtml?more=all&pageIndex=' + str(page_index)+'&selectedNavigationName=RecruitmentInfoMain&selectedItem=jobFair'
        try:

            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            tables = soup.find_all("table")
            trs = tables[0].find_all("tr")
#             tr = trs[0]
            for tr in trs:
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'北京航天航空大学就业信息网'
                campusTalkInfo.university_name = u'北京航天航空大学'
                campusTalkInfo.university_name_short = u'北航'
                campusTalkInfo.university_name_en = u'buaa-beijing'
                campusTalkInfo.campus_talk_name = unicode(tr.a.string[0:50])
                href_url = u'http://career.buaa.edu.cn' + unicode(tr.a['href'])
                campusTalkInfo.campus_talk_date = tr.span.string[3:19]
                print tr.span.string
                campusTalkInfo.campus_talk_location = unicode(tr.find_all('span')[1]['title'])
                detail_url = href_url
                detail_opener=urllib2.build_opener()
                detail_opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                detail_response = detail_opener.open(detail_url)
                detail_html = detail_response.read()
                detail_soup = BeautifulSoup(detail_html)
                campusTalkInfo.company_introduce = detail_soup.find(class_="calender_style")
                xjh = beihang_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].save()
                else:         
                    campusTalkInfo.save()
        except Exception,e:  
            print str(e)

# def beijingdaxue():
#     beida_list = CampusTalkInfo.objects.filter(university_name_short="北大")
#     for page_index in range(40807, 40807+200):
#         url = 'http://scc.pku.edu.cn/zpxx/zphd/' + str(page_index) + '.htm'
#         try:
#             opener=urllib2.build_opener()
#             opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
#             response = opener.open(url)
#             html = response.read()
#             soup = BeautifulSoup(html)
#             campusTalkInfo = CampusTalkInfo()
#             contentTag = soup.find_all(class_="wz1ul")
#             pTag = contentTag[0].find_all("p")
#             campusTalkInfo.campus_talk_name = unicode(contentTag[0].find(class_="heicu").string)
#             campusTalkInfo.company_name = campusTalkInfo.campus_talk_name.replace(u'2015校园招聘', u'')
#             campusTalkInfo.campus_talk_name = campusTalkInfo.company_name
#             if page_index < 40793:
#                 campusTalkInfo.campus_talk_date = u'2014-'+unicode(pTag[1].find_all("span")[1].string)+u'-'+unicode(pTag[1].find_all("span")[3].string)+ ' '+unicode(pTag[2].find_all("span")[1].contents[0])
#             elif page_index>= 40793 and page_index < 40865:
#                 campusTalkInfo.campus_talk_date = unicode(pTag[1].find_all("span")[1].string) +u'-'+ unicode(pTag[1].find_all("span")[3].string)+u'-'+unicode(pTag[1].find_all("span")[5].string)+ ' '+unicode(pTag[2].find_all("span")[1].contents[0])
#             else :
#                 campusTalkInfo.campus_talk_date = unicode(pTag[1].find_all("span")[1].string) +u'-'+ unicode(pTag[1].find_all("span")[3].string)+u'-'+unicode(pTag[1].find_all("span")[5].string)+ ' '+unicode(pTag[2].find_all("span")[1].contents[0])+unicode(pTag[2].find_all("span")[2].contents[0])
#   
# #             print campusTalkInfo.campus_talk_date
#             campusTalkInfo.campus_talk_location = unicode(pTag[3].find_all("span")[0].contents[0])[4:]
#             campusTalkInfo.company_introduce = soup.find(class_="wz1ul")
#             campusTalkInfo.company_introduce = campusTalkInfo.company_introduce.find_all("li")[2]
#             campusTalkInfo.info_source = u'北京大学就业信息网'
#             campusTalkInfo.university_name = u'北京大学'
#             campusTalkInfo.university_name_short = u'北大'
#             campusTalkInfo.university_name_en = u'pku-beijing'
#             xjh = beida_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
#             if xjh:
#                 if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
#                     xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
#                     xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
#                     xjh[0].save()
#             else:
#                 campusTalkInfo.save()
#         except Exception,e: 
#             print page_index 
#             print str(e)

# def beijingdaxue():
#     beida_list = CampusTalkInfo.objects.filter(university_name_short="北大")
#     opener = urllib2.build_opener()
#     opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
#      
#     for page_index in range(0,1):
#         url = ''
#         if page_index == 0:
#             url = 'http://scc.pku.edu.cn/zpxx/zphd/index.htm'
#         else:
#             url = 'http://scc.pku.edu.cn/zpxx/zphd/index' + str(page_index) + '.htm'
#         response = opener.open(url)
#         html = response.read()
#         soup = BeautifulSoup(html) 
#         campusTalkList =   soup.find(id="right").find_all(style="font-size:12px;")
#         print len(campusTalkList)
#         for campusTalk in campusTalkList:
#             campusTalkInfo = CampusTalkInfo()
#             campusTalkInfo.info_source = u'北京大学就业信息网'
#             campusTalkInfo.university_name = u'北京大学'
#             campusTalkInfo.university_name_short = u'北大'
#             campusTalkInfo.university_name_en = u'pku-beijing'
#             campusTalkInfo.campus_talk_name = unicode(campusTalk.a.string)
#             campusTalkInfo.href_url = u'http://scc.pku.edu.cn' + unicode(campusTalk.a['href'])
#             detail_url = campusTalkInfo.href_url
#             detail_opener=urllib2.build_opener()
#             detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
#             detail_response = detail_opener.open(detail_url)
#             detail_html = detail_response.read()
#             detail_soup = BeautifulSoup(detail_html)
#             print detail_soup
#             xjh = beida_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
#             if xjh:
#                 if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
#                     xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
#                     xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
#                     xjh[0].save()
#                 else:
#                      
#                     campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
#                     campusTalkInfo.save()
            
            
             

def beijingligong():
    beijingligong_list = CampusTalkInfo.objects.filter(university_name_short="北京理工")

    for page_index in range(600, 600+200):
        url = 'http://job.bit.edu.cn/employment-activities.html?tx_extevent_pi1%5Bcmd%5D=preview&tx_extevent_pi1%5Buid%5D=' + str(page_index)
        try:
            opener=urllib2.build_opener()
            opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campusTalkInfo = CampusTalkInfo()
            campusTalkInfo.info_source = u'北京理工大学就业信息网'
            campusTalkInfo.university_name = u'北京理工大学'
            campusTalkInfo.university_name_short = u'北京理工'
            campusTalkInfo.university_name_en = u'bit-beijing'
            event_preview = soup.find(id="event_preview")
            campusTalkInfo.campus_talk_name = unicode(event_preview.find("h1").string)
            p_list = event_preview.find_all("p")
            campusTalkInfo.campus_talk_date = unicode(p_list[1].string[6:])
            campusTalkInfo.campus_talk_location = unicode(p_list[3].contents[2][2:])
            campusTalkInfo.company_introduce = event_preview.find(class_="event_content")
            if campusTalkInfo.company_introduce.contents:
                xjh = beijingligong_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    campusTalkInfo.save()
        except Exception,e: 
            print page_index
            print str(e) 


def beijingkeji():
    beijingkeji_list = CampusTalkInfo.objects.filter(university_name_short="北京科大")
    
    for page_index in range(500, 500 + 200):
        url = 'http://job.ustb.edu.cn/front/zph.jspa?channelId=763&tid=' + str(page_index)
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            content = soup.find(class_="dw_xinxi")
            campusTalkInfo = CampusTalkInfo()
            campusTalkInfo.info_source = u'北京科技大学就业信息网'
            campusTalkInfo.university_name = u'北京科技大学'
            campusTalkInfo.university_name_short = u'北京科大'
            campusTalkInfo.university_name_en = u'ustb-beijing'
            campusTalkInfo.campus_talk_name = unicode(content.find("h2").string).replace(u'2015校园招聘会', u'')
            campusTalkInfo.campus_talk_name = campusTalkInfo.campus_talk_name.replace(u'2015校园招聘会', u'')
            dateString = join(content.find_all("td")[1].string.split())
            campusTalkInfo.campus_talk_date = u'2014-' + dateString[0:2] + u'-' + dateString[3:5] + u' ' + dateString[7:12]
            campusTalkInfo.campus_talk_location = unicode(join(content.find_all("td")[2].string.split()))
            campusTalkInfo.company_introduce = content.find(class_ = "m_text")
            campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
#             print campusTalkInfo.company_introduce.contents

            if campusTalkInfo.company_introduce.contents:
                xjh = beijingkeji_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
#                         xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
#             raise
        else:
            print str(page_index)+':成功'

#原始网站过于复杂，从海投网获取数据
def beijingjiaotong():
    
    beijingjiaoda_list = CampusTalkInfo.objects.filter(university_name="北京交通大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+1):
        try:
            url = 'http://xjh.haitou.cc/bj/uni-17/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
#             print soup
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'北京交通大学就业咨询网'
                campusTalkInfo.university_name = u'北京交通大学'
                campusTalkInfo.university_name_short = u'北京交大'
                campusTalkInfo.university_name_en = u'bjtu-beijing'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])
                
                xjh = beijingjiaoda_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'
    
def shanghaijiaotongdaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="上海交通大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+6):
        try:
            url = 'http://xjh.haitou.cc/sh/uni-132/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'上海交通大学学生就业服务和职业发展中心'
                campusTalkInfo.university_name = u'上海交通大学'
                campusTalkInfo.university_name_short = u'上海交大'
                campusTalkInfo.university_name_en = u'sjtu-shanghai'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功' 
            
def tongjidaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="同济大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+6):
        try:
            url = 'http://xjh.haitou.cc/sh/uni-134/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'同济大学学生就业信息网'
                campusTalkInfo.university_name = u'同济大学'
                campusTalkInfo.university_name_short = u'同济'
                campusTalkInfo.university_name_en = u'tongji-shanghai'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)

                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功' 

def fudandaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="复旦大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+5):
        try:
            url = 'http://xjh.haitou.cc/sh/uni-133/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
#             print soup
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'复旦大学学生就业信息网'
                campusTalkInfo.university_name = u'复旦大学'
                campusTalkInfo.university_name_short = u'复旦'
                campusTalkInfo.university_name_en = u'fudan-shanghai'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'
            
def shanghaidaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="上海大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+3):
        try:
            url = 'http://xjh.haitou.cc/sh/uni-105/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
#             print soup
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'上海大学就业网'
                campusTalkInfo.university_name = u'上海大学'
                campusTalkInfo.university_name_short = u'上大'
                campusTalkInfo.university_name_en = u'shu-shanghai'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'            


def donghuadaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="东华大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+5):
        try:
            url = 'http://xjh.haitou.cc/sh/uni-138/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
#             print soup
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'东华大学学生就业服务中心'
                campusTalkInfo.university_name = u'东华大学'
                campusTalkInfo.university_name_short = u'东华'
                campusTalkInfo.university_name_en = u'dhu-shanghai'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
#                     print campusTalkInfo.company_introduce
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功' 
            
def huananligongdaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="华南理工大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+7):
        try:
            url = 'http://xjh.haitou.cc/gz/uni-34/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'华南理工大学就业在线'
                campusTalkInfo.university_name = u'华南理工大学'
                campusTalkInfo.university_name_short = u'华工'
                campusTalkInfo.university_name_en = u'scut-guangzhou'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'             
            

def guangzhoudaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="广州大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+5):
        try:
            url = 'http://xjh.haitou.cc/gz/uni-35/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'广州大学招生就业工作处'
                campusTalkInfo.university_name = u'广州大学'
                campusTalkInfo.university_name_short = u'广大'
                campusTalkInfo.university_name_en = u'gzhu-guangzhou'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'
            
def guangzhougongyedaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="广东工业大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+5):
        try:
            url = 'http://xjh.haitou.cc/gz/uni-36/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'广东工业大学就业信息中心'
                campusTalkInfo.university_name = u'广东工业大学'
                campusTalkInfo.university_name_short = u'广工'
                campusTalkInfo.university_name_en = u'gdut-guangzhou'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'
  
def jinandaxue():
    qinghua_list = CampusTalkInfo.objects.filter(university_name="暨南大学")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
        
    for page_index in range(1,1+5):
        try:
            url = 'http://xjh.haitou.cc/gz/uni-33/after/hold/page-'+ str(page_index) +'/'
            response = opener.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            campus_talk_name_list = soup.find_all(class_="preach-tbody-title")
            campus_talk_date_list = soup.find_all(class_="hold-ymd")
            campus_talk_location_list = soup.find_all(class_="preach-tbody-addre")
            for i in range(len(campus_talk_name_list)):
    
                campusTalkInfo = CampusTalkInfo()
                campusTalkInfo.info_source = u'暨南大学学生就业指导信息网'
                campusTalkInfo.university_name = u'暨南大学'
                campusTalkInfo.university_name_short = u'暨大'
                campusTalkInfo.university_name_en = u'jnu-guangzhou'
                campusTalkInfo.campus_talk_name = unicode(campus_talk_name_list[i].find("company").string)
                campusTalkInfo.company_name = campusTalkInfo.campus_talk_name
                campusTalkInfo.campus_talk_date = unicode(campus_talk_date_list[2*i].string)
                if len(campus_talk_location_list[i].string) > 22:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string[:22]) + u'...'
                else:
                    campusTalkInfo.campus_talk_location = unicode(campus_talk_location_list[i].string)
                campusTalkInfo.href_url = u'http://xjh.haitou.cc' + unicode(campus_talk_name_list[i].a['href'])

                xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
                else:
                    detail_url = campusTalkInfo.href_url
                    detail_opener=urllib2.build_opener()
                    detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                    detail_response = detail_opener.open(detail_url)
                    detail_html = detail_response.read()
                    detail_soup = BeautifulSoup(detail_html)
                    campusTalkInfo.company_introduce = detail_soup.find(class_="panel-body panel-body-text")
                    campusTalkInfo.save()
        except Exception,e:
            print str(e)
        else:
            print str(page_index)+':成功'
  
# 中山大学        
def zhongshandaxue():
    url = 'http://xjh.yjbys.com/sysu/'

    try:
        opener=urllib2.build_opener()
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        response = opener.open(url)
        html = response.read()
        soup = BeautifulSoup(html,from_encoding="gb18030")
#         print soup
        qinghua_list = CampusTalkInfo.objects.filter(university_name="中山大学")
        
        for tr in soup.table.find_all("tr"):
            if tr.find("th"):
                continue
            td_list = tr.find_all("td")
            campusTalkInfo = CampusTalkInfo()
            campusTalkInfo.campus_talk_name = unicode(td_list[3].find("a").string)
#             print td_list[3]
#             print campusTalkInfo.campus_talk_name
            
            if td_list[2].string:
                end = td_list[2].string.find('-')
                if end > 0:
                    campusTalkInfo.campus_talk_date = unicode(td_list[1].string[0:10].strip())+' '+unicode(td_list[2].string[0:end].strip())
#                 print campusTalkInfo.campus_talk_date
                elif td_list[2].string.find(':') >0:
                    campusTalkInfo.campus_talk_date = unicode(td_list[1].string[0:10].strip())+' '+unicode(td_list[2].string.strip())
                else:
                    campusTalkInfo.campus_talk_date = None
            else: 
                campusTalkInfo.campus_talk_date = None
                
            
            campusTalkInfo.info_source = u'中山大学毕业生就业信息网'
            campusTalkInfo.university_name = u'中山大学'
            campusTalkInfo.university_name_short = u'中大'
            campusTalkInfo.campus_talk_location = unicode(td_list[5].find("font").string)
            campusTalkInfo.university_name_en = u'sysu-guangzhou'
            campusTalkInfo.href_url = u'http://www.yjbys.com/mingqi' + unicode(td_list[3].a['href']) + u'#job'
#             print campusTalkInfo.href_url
            
            xjh = qinghua_list.filter(campus_talk_name=campusTalkInfo.campus_talk_name)
            if xjh:
                if xjh:
                    if xjh[0].campus_talk_date != campusTalkInfo.campus_talk_date or xjh[0].campus_talk_location != campusTalkInfo.campus_talk_location:
                        xjh[0].campus_talk_date = campusTalkInfo.campus_talk_date
                        xjh[0].campus_talk_location = campusTalkInfo.campus_talk_location
                        xjh[0].save()
            else:
                
                detail_url = campusTalkInfo.href_url
                detail_opener=urllib2.build_opener()
                detail_opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
                detail_response = detail_opener.open(detail_url)
                detail_html = detail_response.read()
                detail_soup = BeautifulSoup(detail_html)
                campusTalkInfo.company_introduce = detail_soup.find(id="section").find(class_="col")
#                 print campusTalkInfo.company_introduce
                campusTalkInfo.save()
    except Exception,e:  
        print str(e)    
    else:
        print '成功'
  
  
# zhongshandaxue()          
# donghuadaxue()           
# shanghaidaxue()
# fudandaxue()
# tongjidaxue()            
# shanghaijiaotongdaxue()            
# qinghuadaxue()
# beijingjiaotong()    
# beijingkeji()
# beijingligong()
# beijingdaxue()
# beihang()
