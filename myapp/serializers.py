import logging
import django.contrib.auth
from rest_framework import serializers
import myapp.models as models

logger = logging.getLogger('mylogger')

class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = django.contrib.auth.models.User
        fields = ('username', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    class Meta:
        model = models.Profile
        fields = ('user', 'display_name')
        read_only = ('display_name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'description')
        read_only = ('description',)


class ListingSerializer(serializers.ModelSerializer):
    owners = ProfileSerializer(required=False, many=True)
    # TODO: how to indicate that this should look for an existing category?
    # category = CategorySerializer(required=False, validators=[])
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Category.objects.all()
    )


    class Meta:
        model = models.Listing
        depth = 2
        fields = [
            'title',
            'owners',
            'category',
            ]
    def validate(self, data):
        logger.info('inside ListingSerializer validate')
        return data

    def create(self, validated_data):
        logger.info('inside ListingSerializer.create')
        # not even getting this far...