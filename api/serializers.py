from django.contrib.auth.models import User, Group
from catalog.models import GoodItem
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GoodItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodItem
        fields = ['url', 'created_at', 'title', 'price', 'vendor', 'unit_of_measure']


class StatDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sent = serializers.IntegerField()
    time = serializers.CharField(max_length=60)
    connection_count = serializers.IntegerField()

