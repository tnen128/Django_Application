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
