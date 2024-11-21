from django.db import models
from django.core.exceptions import ValidationError

class MapImage(models.Model):
    image_url = models.ImageField(upload_to='images/map')
    latitude = models.FloatField(default=0.0, null=False, blank=False)
    longitude = models.FloatField(default=0.0, null=False, blank=False)
    area_m2 = models.FloatField(default=0.0, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"MapPanel {self.id}"

class PolygonDataValidator:
    def __init__(self, limit_value=None):
        self.limit_value = limit_value

    def deconstruct(self):
        """Make the validator serializable for migrations"""
        path = 'panel.models.PolygonDataValidator'
        args = []
        kwargs = {'limit_value': self.limit_value}
        return (path, args, kwargs)

    def check_polygon_format(self, polygon):
        # 필수 키 확인
        required_keys = {'all_points_x', 'all_points_y'}
        if not isinstance(polygon, dict) or not all(key in polygon for key in required_keys):
            return False
        
        # x, y 배열의 길이가 같은지 확인
        if len(polygon['all_points_x']) != len(polygon['all_points_y']):
            return False
            
        # 모든 값이 숫자인지 확인
        if not all(isinstance(x, (int, float)) for x in polygon['all_points_x']):
            return False
        if not all(isinstance(y, (int, float)) for y in polygon['all_points_y']):
            return False
            
        return True

    def __call__(self, value):
        if not isinstance(value, list):
            raise ValidationError('Polygon data must be a list')
        
        for polygon in value:
            if not self.check_polygon_format(polygon):
                raise ValidationError(
                    'Each polygon must be an object with "all_points_x" and "all_points_y" arrays of numbers'
                )

class GameImage(models.Model):
    image_url = models.ImageField(upload_to='images/game')
    polygon = models.JSONField(
        default=list,
        validators=[PolygonDataValidator()],
        help_text='List of polygons. Each polygon contains all_points_x and all_points_y arrays'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"GamePanel {self.id}"

class GameScore(models.Model):
    image_url = models.ImageField(upload_to='images/profile')
    nickname = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-score']  # Default ordering by score descending

    def __str__(self):
        return f"Nickname: {self.nickname} - UUID: {self.uuid} - Score: {self.score}"

class GameClaimPolygon(models.Model):
    user_uuid = models.CharField(max_length=100)
    image_id = models.IntegerField()
    game_id = models.CharField(max_length=100)
    round = models.IntegerField()
    polygon = models.JSONField(
        validators=[PolygonDataValidator()],
        help_text='Polygon containing all_points_x and all_points_y arrays'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.game_id} - Round {self.round} - User {self.user_uuid}"

class GameClaimMark(models.Model):
    user_uuid = models.CharField(max_length=100)
    image_id = models.IntegerField()
    game_id = models.CharField(max_length=100)
    round = models.IntegerField()
    mark = models.JSONField(
        help_text='Mark coordinates containing x and y values'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.game_id} - Round {self.round} - User {self.user_uuid}"

