from rest_framework import serializers
from .models import PanelImage

# Serializer for PanelImage
class PanelImageSerializer(serializers.ModelSerializer):
    mean_point_latitude = serializers.FloatField(source='latitude')
    mean_point_longitude = serializers.FloatField(source='longitude')
    shape_area_m2 = serializers.FloatField(source='area_m2')

    class Meta:
        model = PanelImage
        fields = ['id', 'mean_point_latitude', 'mean_point_longitude', 'shape_area_m2']

# Serializer for returning image information
class PanelImageDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PanelImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url) if request else image_url
