from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/map/panels', CoordinatesView.as_view()),
    path('api/v1/game/image', GameImageView.as_view()),
    path('api/v1/game/score', GameScoreView.as_view()),
    path('api/v1/game/ranking', GameRankingView.as_view()),
    path('api/v1/game/claim/polygon', GameClaimPolygonView.as_view()),
    path('api/v1/game/claim/mark', GameClaimMarkView.as_view()),
]