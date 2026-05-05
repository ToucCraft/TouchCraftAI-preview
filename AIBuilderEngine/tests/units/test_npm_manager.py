import pytest
from unittest.mock import patch, MagicMock
from services.npm_manager import NPMManager


@patch('services.npm_manager.requests.post')
def test_npm_manager_auth(mock_requests_post):
    """
    Test: Verify that NPMManager correctly retrieves the auth token on init.
    """
    # Setup mock response for auth endpoint
    mock_response = MagicMock()
    mock_response.json.return_value = {"token": "mocked-jwt-token"}
    mock_requests_post.return_value = mock_response

    npm = NPMManager("http://mock-api.local", "admin@test.com", "password")

    assert npm.token == "mocked-jwt-token"
    mock_requests_post.assert_called_once()


@patch('services.npm_manager.requests.post')
@patch('services.npm_manager.requests.put')
def test_create_proxy_host(mock_requests_put, mock_requests_post):
    """
    Test: Verify that create_proxy_host sends the correct payload to Nginx Proxy Manager.
    """
    # Setup auth mock
    mock_auth_response = MagicMock()
    mock_auth_response.json.return_value = {"token": "mocked-jwt-token"}

    # Setup proxy host creation mock
    mock_create_response = MagicMock()
    mock_create_response.status_code = 201
    mock_create_response.json.return_value = {"id": 10, "certificate_id": 5}

    # Assign responses to sequential post calls (1st for auth, 2nd for proxy creation)
    mock_requests_post.side_effect = [mock_auth_response, mock_create_response]

    npm = NPMManager("http://mock-api.local", "admin@test.com", "password")
    result = npm.create_proxy_host("client-domain.com", "container-123", port=80)

    assert result["id"] == 10
    # Verify that a PUT request was made to enforce SSL settings
    mock_requests_put.assert_called_once()
