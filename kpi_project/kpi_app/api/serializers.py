# kpi_app/serializers.py

from rest_framework import serializers
from ..models.models import KPI, Asset, AssetKPI

class KPISerializer(serializers.ModelSerializer):
    """Serializes the KPI model for API responses"""
    class Meta:
        model = KPI
        fields = ['id', 'name', 'expression', 'description']

class AssetSerializer(serializers.ModelSerializer):
    """Serializes the Asset model for API responses"""
    class Meta:
        model = Asset
        fields = ['id', 'asset_id', 'name']

class AssetKPISerializer(serializers.ModelSerializer):
    """Serializes the AssetKPI model for API responses"""
    class Meta:
        model = AssetKPI
        fields = ['id', 'kpi', 'asset', 'attribute_id']
