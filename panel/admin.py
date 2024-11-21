from django.contrib import admin
from .models import GameClaimMark, GameImage, GameClaimPolygon, MapImage, GameScore
admin.site.register(MapImage)
admin.site.register(GameScore)
admin.site.register(GameClaimPolygon)
admin.site.register(GameClaimMark)
admin.site.register(GameImage)
# Register your models here.
