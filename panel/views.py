from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import GameImage, MapImage, GameScore
from .serializers import MapPanelFullSerializer
from rest_framework import status

# View to return all coordinates
class CoordinatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        panels = MapImage.objects.all()
        serializer = MapPanelFullSerializer(
            panels, 
            many=True,
            context={'request': request}  # request 객체를 context로 전달
        )
        return Response({'panel': serializer.data})

class GameImageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        panels = GameImage.objects.all()
        panel = panels.first()
        data = {
            'id': panel.id,
            'image_url': request.build_absolute_uri(panel.image_url.url),
            'polygon': panel.polygon
        } 
        return Response(data)

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

            GameScore.objects.create(
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
            rankings = GameScore.objects.order_by('-score')[:10]  # Get top 10 scores
            
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