from django.db import models

class PanelImage(models.Model):
    image = models.ImageField(upload_to='images/')
    latitude = models.FloatField(default=0.0, null=False, blank=False)
    longitude = models.FloatField(default=0.0, null=False, blank=False)
    area_m2 = models.FloatField(default=0.0, null=False, blank=False)

    def __str__(self):
        return f"PanelImage {self.id}"
