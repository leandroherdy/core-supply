import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture(scope="module")
def client():
    """
    Fixture to provide an API client efficiently for multiple tests.
    We use scope=module to ensure that the client is only created once per test module.
    """
    return APIClient()


class TestProcessDataViewJson:
    url_json = "/api/v1/clients/https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json/"

    @pytest.mark.django_db
    def test_status_processar_dados_json(self, client):
        """
        Test if the API responds with HTTP status 200 for JSON data.
        """
        response = client.get(self.url_json, {"page": 1, "page_size": 10})
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_pagination_structure_json(self, client):
        """
        Test if the API responds with the correct pagination fields for JSON data.
        """
        response = client.get(self.url_json, {"page": 1, "page_size": 10})
        data = response.json()

        assert "pageNumber" in data
        assert "pageSize" in data
        assert "totalCount" in data
        assert "users" in data
        assert len(data["users"]) <= 10

    @pytest.mark.django_db
    def test_data_structure_json(self, client):
        """
        Test if each item in 'users' has the correct data structure for JSON data.
        """
        response = client.get(self.url_json, {"page": 1, "page_size": 10})
        data = response.json()

        if data["users"]:
            item = data["users"][0]
            assert "type" in item
            assert "gender" in item
            assert "name" in item
            assert "location" in item
            assert "email" in item
            assert "birthday" in item
            assert "registered" in item
            assert "telephoneNumbers" in item
            assert "mobileNumbers" in item
            assert "picture" in item
            assert "nationality" in item
