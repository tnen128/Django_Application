from django.db import models

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
