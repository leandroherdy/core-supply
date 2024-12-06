#!/bin/bash

AUTH_TOKEN=""
BASE_API_URL="http://127.0.0.1:8000/api/v1/clients/"

QUERY_PARAMS="?page=1&page_size=10"

validate_response() {
  local additional_params=$1
  local full_url="${BASE_API_URL}${QUERY_PARAMS}${additional_params}"

  echo "Testing URL: $full_url"

  response=$(curl -s -H "Authorization: Token $AUTH_TOKEN" -H "Content-Type: application/json" "$full_url")
  status_code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Token $AUTH_TOKEN" -H "Content-Type: application/json" "$full_url")

  echo "API Response: $response"

  if [ "$status_code" -eq 200 ]; then
    echo "Status code is 200 OK."
  else
    echo "Unexpected status code: $status_code"
    echo "-------------------------------------"
    return
  fi

  if echo "$response" | grep -q '"pageNumber"' && \
     echo "$response" | grep -q '"pageSize"' && \
     echo "$response" | grep -q '"totalCount"' && \
     echo "$response" | grep -q '"users"'; then
    echo "Response body structure is valid."
  else
    echo "Response body structure is invalid."
  fi

  echo "-------------------------------------"
}

validate_response ""
validate_response "&type=type1"
validate_response "&region=Norte"
validate_response "&type=type1&region=Norte"
