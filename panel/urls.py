from django.urls import path
from .views import CoordinatesView, PanelImageView

urlpatterns = [
    path('api/v1/coordinates/', CoordinatesView.as_view(), name='coordinates'),
    path('api/v1/panel-image/<int:id>/', PanelImageView.as_view(), name='panel-image'),
]