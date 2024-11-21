from django.contrib import admin
from .models import GameMarkerBugReport, GamePanel, GamePolygonBugReport, MapPanel, GameUserScore
admin.site.register(MapPanel)
admin.site.register(GameUserScore)
admin.site.register(GamePolygonBugReport)
admin.site.register(GameMarkerBugReport)
admin.site.register(GamePanel)
# Register your models here.
