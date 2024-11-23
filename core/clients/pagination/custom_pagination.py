from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination with configurable page size and response structure.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Returns a custom paginated response with previous and next page URLs.

        Args: data (list): Paginated data.

        Returns: Response: Pagination details, including page number, page size, total count,
        previous page URL, next page URL, and data.
        """
        request = self.request

        previous_page_url = self.get_previous_page_url(request) if self.page.has_previous() else None
        next_page_url = self.get_next_page_url(request) if self.page.has_next() else None

        return Response({
            "pageNumber": self.page.number,
            "pageSize": self.page.paginator.per_page,
            "totalCount": self.page.paginator.count,
            "previousPage": previous_page_url,
            "nextPage": next_page_url,
            "users": data
        })

    def get_previous_page_url(self, request):
        """
        Returns the URL for the previous page.

        Args: request: The request object.

        Returns: str: The URL for the previous page.
        """
        previous_page_number = self.page.previous_page_number()
        return request.build_absolute_uri(self.get_page_url(previous_page_number))

    def get_next_page_url(self, request):
        """
        Returns the URL for the next page.

        Args: request: The request object.

        Returns: str: The URL for the next page.
        """
        next_page_number = self.page.next_page_number()
        return request.build_absolute_uri(self.get_page_url(next_page_number))

    def get_page_url(self, page_number):
        """
        Generates the URL for a specific page number.

        Args: page_number: The page number to generate the URL for.

        Returns: str: The URL for the given page number.
        """
        url = self.request.path
        return f"{url}?page={page_number}&page_size={self.page_size}"
