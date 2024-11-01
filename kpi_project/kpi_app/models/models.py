"""
Models for KPI application.
"""

from django.db import models

class KPI(models.Model):
    """
    Represents a Key Performance Indicator (KPI) entity with an expression.
    """
    name = models.CharField(max_length=100)
    expression = models.TextField()  # Stores the equation or formula
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    """
    Represents an Asset (e.g., a sensor) entity.
    """
    asset_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AssetKPI(models.Model):
    """
    Represents the relationship between an Asset and a KPI, with an attribute ID.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    attribute_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.asset.name} - {self.kpi.name} (Attribute: {self.attribute_id})"

class EvaluationLog(models.Model):
    """
    Logs the evaluation of KPIs for assets over time.
    """
    asset_id = models.CharField(max_length=100)
    attribute_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    result = models.FloatField()

    def __str__(self):
        return f"EvaluationLog(asset_id={self.asset_id}, attribute_id={self.attribute_id}, result={self.result})"
