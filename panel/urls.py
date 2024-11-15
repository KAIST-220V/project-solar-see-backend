from django.urls import path
from .views import CoordinatesView, PanelImageView

urlpatterns = [
    path('v1/coordinates/', CoordinatesView.as_view(), name='coordinates'),
    path('v1/panel-image/<int:id>/', PanelImageView.as_view(), name='panel-image'),
]