def apply_filters(request, data):
    """
    Apply filters to the data based on query parameters and validate invalid parameters.

    :param request: The HTTP request containing query parameters.
    :param data: The list of data to be filtered.
    :return: Filtered data or an error response.
    """
    valid_filters = {"type", "region", "page", "page_size"}

    invalid_filters = set(request.query_params.keys()) - valid_filters
    if invalid_filters:
        return {"error": f"Invalid filter parameter(s): {', '.join(invalid_filters)}"}, 400

    # Apply filter by type
    type_filter = request.query_params.get('type')
    if type_filter:
        types = type_filter.split(',')  # Allow multiple types separated by commas
        data = [item for item in data if item['type'] in types]

    # Apply filter by region
    region_filter = request.query_params.get('region')
    if region_filter:
        regions = region_filter.split(',')  # Allow multiple regions separated by commas
        data = [item for item in data if item['location']['region'] in regions]

    return {"users": data, "totalCount": len(data)}, 200
