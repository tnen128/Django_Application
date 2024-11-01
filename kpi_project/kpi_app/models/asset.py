from django.db import models

class Asset(models.Model):
    """
    Represents an Asset (e.g., a sensor) entity.
    """
    asset_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
