from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import MapPanel, GameUserScore
from .serializers import PanelImageSerializer, PanelImageDetailSerializer
from rest_framework import status



# View to return all coordinates
class CoordinatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        panels = MapPanel.objects.all()
        serializer = PanelImageSerializer(panels, many=True)
        return Response({'panel': serializer.data})
    
class PanelImageView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PanelImageDetailSerializer

    def get(self, request, id):
        panel_image = get_object_or_404(MapPanel, id=id)
        serializer = self.serializer_class(panel_image, context={'request': request})
        return Response(serializer.data)

class GameImageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Implement game image retrieval logic
        pass

class GameScoreView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            nickname = request.data.get('nickname')
            uuid = request.data.get('uuid') 
            score = request.data.get('score')

            if not all([nickname, uuid, score]):
                return Response(
                    {"error": "Missing required fields"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create new game score record
            GameUserScore.objects.create(
                nickname=nickname,
                uuid=uuid,
                score=score
            )

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameRankingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Assuming you have a GameScore model with fields: image_url, nickname, score
            # Get top scores ordered by score in descending order
            rankings = GameUserScore.objects.order_by('-score')[:10]  # Get top 10 scores
            
            ranking_data = [{
                'image_url': score.image_url or "/media/images/default_profile.png",
                'nickname': score.nickname,
                'score': score.score
            } for score in rankings]
            
            return Response({'ranking': ranking_data})
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameClaimPolygonView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Implement polygon claim logic
        pass

class GameClaimMarkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Implement mark claim logic
        pass