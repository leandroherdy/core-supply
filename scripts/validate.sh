#!/bin/bash

# Defina a URL da API e o token de autenticação
AUTH_TOKEN=""
JSON_API_URL="http://127.0.0.1:8000/api/v1/clients/https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json/?page=1&page_size=10"
CSV_API_URL="http://127.0.0.1:8000/api/v1/clients/https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv/?page=1&page_size=10"

validate_response() {
  local url=$1
  echo "Testing URL: $url"

  # Make the API call and capture the response
  response=$(curl -s -H "Authorization: Token $AUTH_TOKEN" -H "Content-Type: application/json" "$url")
  echo "API Response: $response"

  # Validate the response body structure using grep and awk
  if echo "$response" | grep -q '"pageNumber"' && \
     echo "$response" | grep -q '"pageSize"' && \
     echo "$response" | grep -q '"totalCount"' && \
     echo "$response" | grep -q '"users"'; then
    echo "Response body structure is valid."
  else
    echo "Response body structure is invalid."
  fi

  status_code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Token $AUTH_TOKEN" -H "Content-Type: application/json" "$url")
  if [ "$status_code" -eq 200 ]; then
    echo "Status code is 200 OK."
  else
    echo "Unexpected status code: $status_code"
  fi

  echo "-------------------------------------"
}

validate_response "$JSON_API_URL"

validate_response "$CSV_API_URL"
