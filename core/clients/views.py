from django.apps import apps
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.clients.filter.filter_data import apply_filters
from core.clients.pagination.custom_pagination import CustomPagination


@extend_schema(
    summary="Get filtered clients",
    description=(
        "Retrieve preloaded client data or apply multiple filters ('type' and 'region') "
        "to generate a customized, paginated dataset. Supports filtering by client type "
        "(e.g., 'laborious', 'normal', 'special') and region (e.g., 'norte', 'nordeste', "
        "'centro-oeste', 'sudeste', 'sul'). "
        "Multiple values can be provided for each filter, separated by commas."
    ),
    parameters=[
        OpenApiParameter(
            name="type",
            description=(
                "Filter by client type (comma-separated, e.g., 'laborious,normal,special'). "
                "Allowed values: 'laborious', 'normal', 'special'."
            ),
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="region",
            description=(
                "Filter by region (comma-separated, e.g., 'sul,norte'). "
                "Allowed values: 'norte', 'nordeste', 'centro-oeste', 'sudeste', 'sul'."
            ),
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="page",
            description="Page number for pagination (default: 1).",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="page_size",
            description="Page size for pagination (default: 10).",
            required=False,
            type=int,
        ),
    ],
)
@api_view(['GET'])
def get_filtered_clients(request):
    """
    Handles GET requests to retrieve and filter preloaded data.

    This view fetches data stored in memory, applies optional filters
    for 'type' and 'region' based on query parameters, and returns the
    results in a paginated response.

    Query Parameters:
        - type (str): Filter data by client type (comma-separated for multiple regions).
        - region (str): Filter data by region (comma-separated for multiple regions).

    Returns:
        - 200: Paginated filtered data.
        - 404: If no data is available.
        - 500: If the data processor is not initialized.
    """
    try:
        data_processor = apps.get_app_config('clients').data_processor
        data = data_processor.get_data()
    except (LookupError, AttributeError):
        return Response({'error': 'Data processor is not initialized.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_data, status_code = apply_filters(request, data)

    if status_code == 400:
        return Response(response_data, status=status_code)

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(response_data["users"], request)
    return paginator.get_paginated_response(result_page)
