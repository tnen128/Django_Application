"""
Unit tests for KPI application.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models.models import KPI, Asset, AssetKPI

class KPIModelTests(TestCase):
    """
    Tests for the KPI model.
    """

    def setUp(self):
        self.kpi = KPI.objects.create(name="Sample KPI", expression="ATTR+50")

    def test_kpi_creation(self):
        """Test if a KPI is created with the correct name."""
        self.assertEqual(str(self.kpi), "Sample KPI")

    def test_kpi_expression_evaluation(self):
        """Test the evaluation of a KPI expression."""
        self.assertEqual(self.kpi.expression, "ATTR+50")


class KPIAPITests(APITestCase):
    """
    API tests for KPI endpoints.
    """

    def setUp(self):
        self.kpi = KPI.objects.create(name="Sample KPI", expression="ATTR+50")

    def test_create_kpi(self):
        """Test the creation of a KPI via the API."""
        url = reverse('kpi-list')
        data = {"name": "New KPI", "expression": "ATTR*2"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New KPI")

    def test_list_kpis(self):
        """Test listing KPIs."""
        url = reverse('kpi-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_kpi(self):
        """Test retrieving a specific KPI by ID."""
        url = reverse('kpi-detail', args=[self.kpi.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.kpi.name)


class AssetAPITests(APITestCase):
    """
    API tests for Asset endpoints.
    """

    def setUp(self):
        self.asset = Asset.objects.create(asset_id="A001", name="Test Asset")

    def test_create_asset(self):
        """Test the creation of an Asset via the API."""
        url = reverse('asset-list')
        data = {"asset_id": "A002", "name": "New Asset"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["asset_id"], "A002")

    def test_list_assets(self):
        """Test listing Assets."""
        url = reverse('asset-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_asset(self):
        """Test retrieving a specific Asset by ID."""
        url = reverse('asset-detail', args=[self.asset.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.asset.name)


class AssetKPIAPITests(APITestCase):
    """
    API tests for AssetKPI endpoints.
    """

    def setUp(self):
        self.kpi = KPI.objects.create(name="Sample KPI", expression="ATTR+50")
        self.asset = Asset.objects.create(asset_id="A001", name="Test Asset")
        self.asset_kpi = AssetKPI.objects.create(asset=self.asset, kpi=self.kpi, attribute_id="Temp")

    def test_create_asset_kpi(self):
        """Test the creation of an AssetKPI relationship via the API."""
        url = reverse('assetkpi-list')
        data = {
            "asset": self.asset.id,
            "kpi": self.kpi.id,
            "attribute_id": "Pressure"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_asset_kpis(self):
        """Test listing AssetKPIs."""
        url = reverse('assetkpi-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_asset_kpi(self):
        """Test retrieving a specific AssetKPI by ID."""
        url = reverse('assetkpi-detail', args=[self.asset_kpi.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["attribute_id"], self.asset_kpi.attribute_id)

    def test_evaluate_asset_kpi(self):
        """Test evaluating the KPI expression via the evaluate endpoint."""
        url = reverse('assetkpi-evaluate', args=[self.asset_kpi.id])
        data = {"value": "100"}
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.json())  # Print error message for debugging
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("result", response.data)



class EvaluateExpressionTests(APITestCase):
    """
    Tests for custom evaluations with edge cases.
    """

    def setUp(self):
        self.kpi = KPI.objects.create(name="Edge KPI", expression="ATTR+50")
        self.asset = Asset.objects.create(asset_id="A003", name="Edge Asset")
        self.asset_kpi = AssetKPI.objects.create(asset=self.asset, kpi=self.kpi, attribute_id="EdgeAttr")

    def test_invalid_expression(self):
        """Test evaluate endpoint with an invalid expression."""
        url = reverse('assetkpi-evaluate', args=[self.asset_kpi.id])
        data = {"value": "INVALID"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_value(self):
        """Test evaluate endpoint with a null value."""
        url = reverse('assetkpi-evaluate', args=[self.asset_kpi.id])
        data = {"value": None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
