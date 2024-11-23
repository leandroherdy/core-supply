from urllib.parse import unquote

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.clients.pagination.custom_pagination import CustomPagination
from core.clients.service.client_data_processor import DataProcessor


@api_view(['GET'])
def process_data_view(request, external_url):
    """
    Processes external data from a URL and returns it in a paginated response.

    Args:
        request (HttpRequest): The HTTP request.
        external_url (str): The external URL to fetch and process data from.

    Returns:
        Response: Paginated response with processed data or error message.
    """
    url = unquote(external_url.strip())
    if not url.startswith('http'):
        return Response({'error': 'The URL provided is not valid.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        processed_data = DataProcessor().process_data(url)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(processed_data, request)
    return paginator.get_paginated_response(result_page)
