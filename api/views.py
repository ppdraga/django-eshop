import urllib
import json
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, views
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import UserSerializer, GroupSerializer, GoodItemSerializer, StatDataSerializer

from catalog.models import GoodItem





# Create your views here.


class StatRequest():
    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.full_url = url

    def get_url(self):
        return self.url

    def get_params(self):
        return self.params

    def set_full_url(self, full_url):
        self.full_url = full_url
    
    def get_data(self):
        response = urllib.request.urlopen(self.full_url)
        data = response.read()
        return json.loads(data)


class StatFilterBackend():
    SORTING_FIELDS = ['time', 'total_sent', ]

    def filter_queryset(self, request, stat_request, view):
        stat_params = stat_request.get_params()
        params = {}

        limit = stat_params.get('limit')
        limit = int(limit) if limit else ''

        if limit:
            params['limit'] = limit

        params['user_id'] = request.user.pk

        order_by = stat_params.get('order_by', '')
        if order_by and order_by.startswith('-'):
            order_by = order_by[1:]
        
        if order_by in self.SORTING_FIELDS:
            params[order_by] = stat_params.get('order_by')

        time__gte = stat_params.get('time__gte')
        datetime.strptime(time__gte, '%Y-%m-%d %H:%M:%S')
        if time__gte:
            params['time__gte'] = time__gte

        time__lte = stat_params.get('time__lte')
        datetime.strptime(time__lte, '%Y-%m-%d %H:%M:%S')
        if time__lte:
            params['time__lte'] = time__lte

        params = urllib.parse.urlencode(params)
        print(params)
        if params:
            stat_request.set_full_url(stat_request.get_url() + '?' + params)
        return stat_request



class Pagination(LimitOffsetPagination):
    page_size = 3
    ordering = '-time'
    default_limit = 10000
    max_limit = 10000

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        result = list(queryset[self.offset:self.offset + self.limit + 1])
        self.request = request
        self.count = self.offset + len(result)
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        return result[:self.limit]

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'limit': self.limit,
                'offset': self.offset,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'objects': data
        })



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GoodItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = GoodItem.objects.all()
    serializer_class = GoodItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatView(generics.ListAPIView):
    """
    API endpoint that retrieve data from StatService.
    """
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]
    serializer_class = StatDataSerializer
    # filter_backends = [DjangoFilterBackend,]
    filter_backends = [StatFilterBackend,]
    pagination_class = Pagination


    def get_stat_request(self):
        url = 'http://127.0.0.1:8088/userhour'
        return StatRequest(url, self.request.query_params)


    def list(self, request, *args, **kwargs):
        stat_request = self.filter_queryset(self.get_stat_request())

        data = stat_request.get_data()

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
