from rest_framework import serializers
from .models import MapImage

class MapPanelFullSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MapImage
        fields = ['id', 'image_url', 'latitude', 'longitude', 'area_m2', 
                  'created_at', 'updated_at', 'deleted_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image_url.url
        return request.build_absolute_uri(image_url) if request else image_url
