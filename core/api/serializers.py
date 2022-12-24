from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Provider, ServiceArea


class ProviderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Provider.objects.all())],
        max_length=255)
    phone_number = serializers.CharField(max_length=255)
    language = serializers.CharField(max_length=10)
    currency = serializers.CharField(max_length=20)

    def create(self, validated_data):
        provider = Provider(**validated_data)
        provider.save()
        return provider

    def update(self, obj, validated_data):
        obj.name = validated_data.get('name', obj.name)
        obj.email = validated_data.get('email', obj.email)
        obj.phone_number = validated_data.get('phone_number', obj.phone_number)
        obj.language = validated_data.get('language', obj.language)
        obj.currency = validated_data.get('currency', obj.currency)
        obj.save()
        return obj

    class Meta:
        model = Provider
        fields = '__all__'


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        source="provider", queryset=Provider.objects.all())

    class Meta:
        model = ServiceArea
        geo_field = 'polygon'
        fields = '__all__'
