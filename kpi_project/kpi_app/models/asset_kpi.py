from django.db import models
from .asset import Asset
from .kpi import KPI

class AssetKPI(models.Model):
    """
    Represents the relationship between an Asset and a KPI, with an attribute ID.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    attribute_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.asset.name} - {self.kpi.name} (Attribute: {self.attribute_id})"
