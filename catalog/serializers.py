from catalog.models import GoodItem
from rest_framework import serializers


class GoodItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=255)
    price = serializers.IntegerField(default=0)
    vendor = serializers.CharField(max_length=255)
    unit_of_measure = serializers.CharField(max_length=30)

    def create(self, validated_data):
        """
        Create and return a new `GoodItem` instance, given the validated data.
        """
        return GoodItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `GoodItem` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.unit_of_measure = validated_data.get('unit_of_measure', instance.unit_of_measure)
        instance.save()
        return instance