from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import PanelImage
from .serializers import PanelImageSerializer, PanelImageDetailSerializer



# View to return all coordinates
class CoordinatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        panels = PanelImage.objects.all()
        serializer = PanelImageSerializer(panels, many=True)
        return Response({'panel': serializer.data})
    
class PanelImageView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PanelImageDetailSerializer

    def get(self, request, id):
        panel_image = get_object_or_404(PanelImage, id=id)
        serializer = self.serializer_class(panel_image, context={'request': request})
        return Response(serializer.data)