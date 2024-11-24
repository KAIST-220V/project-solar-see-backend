from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import F, Window
from django.db.models.functions import Rank
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
        while True:
            panels = GameImage.objects.order_by("?")
            panel = panels.first()
            if len(panel.polygon)==0 :
                continue
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
            image_url = request.data.get('image_url')

            if not all([nickname, uuid, score]):
                return Response(
                    {"error": "Missing required fields"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_score = GameScore.objects.create(
                nickname=nickname,
                uuid=uuid,
                score=score,
                image_url=image_url
            )

            ranking_query = GameScore.objects.annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=['score', 'created_at']
                )
            ).filter(id=new_score.id).first()

            if ranking_query:
                rank_position = ranking_query.rank
            else:
                return Response(
                    {"error": "Failed to calculate rank"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {
                    "rank": rank_position,
                    "nickname": new_score.nickname,
                    "score": new_score.score,
                    "uuid": new_score.uuid,
                    "image_url": new_score.image_url
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameRankingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_uuid = request.data.get('uuid')
            if not user_uuid:
                return Response(
                    {"error": "UUID is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 상위 10개의 점수만 가져오기
            GameScore.objects.order_by('-score', 'created_at')

            # 순위 데이터 생성
            ranking_data = []
            for score in rankings:
                ranking_data.append({
                    'image_url': score.image_url,
                    'nickname': score.nickname,
                    'score': score.score,
                    'is_mine': True if score.uuid == user_uuid else False,
                })

            return Response({'ranking': ranking_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
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