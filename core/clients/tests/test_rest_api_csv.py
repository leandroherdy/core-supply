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


class TestProcessDataView:
    base_url = "/api/v1/clients/"

    @pytest.mark.django_db
    def test_status_process_data(self, client):
        """
        Test if the API responds with HTTP status 200 when fetching data.
        """
        response = client.get(self.base_url, {"page": 1, "page_size": 10})
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_filter_by_type(self, client):
        """
        Test if filtering by 'type' works correctly.
        """
        response = client.get(self.base_url, {"type": "type1", "page": 1, "page_size": 10})
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        if data["users"]:
            assert all(item["type"] == "type1" for item in data["users"])

    @pytest.mark.django_db
    def test_filter_by_region(self, client):
        """
        Test if filtering by 'region' works correctly.
        """
        response = client.get(self.base_url, {"region": "Norte", "page": 1, "page_size": 10})
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        if data["users"]:
            assert all(item["location"]["region"] == "Norte" for item in data["users"])

    @pytest.mark.django_db
    def test_filter_by_type_and_region(self, client):
        """
        Test if combining 'type' and 'region' filters works correctly.
        """
        response = client.get(self.base_url, {"type": "type1", "region": "Norte", "page": 1, "page_size": 10})
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        if data["users"]:
            assert all(item["type"] == "type1" and item["location"]["region"] == "Norte" for item in data["users"])

    @pytest.mark.django_db
    def test_filter_with_no_results(self, client):
        """
        Test if the API returns an empty list when no data matches the filters.
        """
        response = client.get(
            self.base_url, {
                "type": "nonexistent_type",
                "region": "InvalidRegion",
                "page": 1,
                "page_size": 10
            }
        )
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "users" in data
        assert data["users"] == []
        assert data["totalCount"] == 0
