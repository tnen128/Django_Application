from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import KPI, Asset, AssetKPI
from .serializers import KPISerializer, AssetSerializer, AssetKPISerializer
from ..core.interpreter import CustomInterpreter  
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class KPIViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Key Performance Indicators (KPIs), allowing users to create, retrieve, update, and delete KPIs.
    """
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all KPIs. Each KPI includes a name, expression, and optional description.",
        responses={200: KPISerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new KPI with a name, an expression (mathematical formula), and an optional description.",
        request_body=KPISerializer,
        responses={201: KPISerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific KPI by its unique ID. Returns the name, expression, and description of the KPI.",
        responses={200: KPISerializer, 404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing KPI by its unique ID. You can update the name, expression, and description.",
        request_body=KPISerializer,
        responses={200: KPISerializer, 404: 'Not Found'}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a KPI by its unique ID.",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AssetViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing Assets, allowing users to create, retrieve, update, and delete assets.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all assets. Each asset has a unique asset ID and name.",
        responses={200: AssetSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new asset with a unique asset ID and name.",
        request_body=AssetSerializer,
        responses={201: AssetSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve an asset by its unique ID. Returns the asset ID and name.",
        responses={200: AssetSerializer, 404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an asset by its unique ID. Allows updating the asset ID and name.",
        request_body=AssetSerializer,
        responses={200: AssetSerializer, 404: 'Not Found'}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an asset by its unique ID.",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AssetKPIViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing the relationships between Assets and KPIs, allowing creation, retrieval, updating, and deletion.
    """
    queryset = AssetKPI.objects.all()
    serializer_class = AssetKPISerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all Asset-KPI relationships. Each entry links an asset to a KPI and has an attribute ID.",
        responses={200: AssetKPISerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new Asset-KPI relationship. Specify an asset ID, KPI ID, and an attribute ID for tracking.",
        request_body=AssetKPISerializer,
        responses={201: AssetKPISerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific Asset-KPI relationship by its unique ID. Returns associated asset, KPI, and attribute ID.",
        responses={200: AssetKPISerializer, 404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an Asset-KPI relationship by its unique ID. Specify the asset ID, KPI ID, and attribute ID.",
        request_body=AssetKPISerializer,
        responses={200: AssetKPISerializer, 404: 'Not Found'}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an Asset-KPI relationship by its unique ID.",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Evaluate the KPI expression for a given Asset-KPI relationship. "
            "Provide the value that will be used to evaluate the expression. "
            "The result will indicate the evaluation outcome."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'value': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The numeric or text input to evaluate in the KPI's expression. This input will replace the 'ATTR' placeholder in the expression."
                )
            },
            required=['value']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'result': openapi.Schema(type=openapi.TYPE_STRING, description="The result of evaluating the KPI expression with the provided value."),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="An error message if the evaluation fails.")
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        """
        Custom action to evaluate the KPI expression for a specific Asset-KPI relationship.
        - **Parameters**: 
          - `value` (string): The input value to evaluate in the expression.
        - **Returns**: 
          - The result of the expression if successful, or an error message if unsuccessful.
        """
        asset_kpi = self.get_object()
        value = request.data.get("value")

        interpreter = CustomInterpreter()
        try:
            result = interpreter.evaluate_expression(asset_kpi.kpi.expression, value)
            return Response({"result": result})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
