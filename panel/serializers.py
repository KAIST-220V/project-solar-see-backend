from rest_framework import serializers
from .models import MapPanel

class MapPanelFullSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MapPanel
        fields = ['id', 'image_url', 'latitude', 'longitude', 'area_m2', 
                 'created_at', 'updated_at', 'deleted_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url) if request else image_url
