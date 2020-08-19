from django.contrib.auth.models import User, Group
from catalog.models import GoodItem
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GoodItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodItem
        fields = ['url', 'created_at', 'title', 'price', 'vendor', 'unit_of_measure']
