__author__ = 'huangtao'


from rest_framework import serializers
from campustalk.models import CampusTalkInfo

class CampusTalkInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CampusTalkInfo
        field = ( 'university_name', 'campus_talk_name', 'url')