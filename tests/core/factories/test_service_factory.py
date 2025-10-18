"""
Unit tests for the service_factory module.

This suite verifies that the create_service factory function behaves correctly,
returning the appropriate service instance for valid inputs and raising
the expected exception for invalid ones.
"""

import pytest

from src.core.factories.service_factory import create_service
from src.services.google.service import GoogleService


@pytest.mark.parametrize(
    "service_name",
    [
        "google",
        "Google",  # Test case-insensitivity
        "GOOGLE",
    ],
)
def test_create_service_google_success(monkeypatch, service_name: str) -> None:
    """
    Verify that `create_service` returns a GoogleService instance for valid names.

    This test uses monkeypatch to set the required environment variables,
    ensuring that the GoogleService can be initialized successfully without
    depending on an external .env file.

    Args:
        monkeypatch: The pytest fixture for modifying environment variables.
        service_name (str): The name of the service to test.
    """
    # ARRANGE: Set dummy environment variables required by GoogleService
    monkeypatch.setenv("GOOGLE_API_KEY", "test_api_key")
    monkeypatch.setenv("GOOGLE_CX", "test_cx_id")

    # ACT: Call the factory function
    service = create_service(service_name=service_name)

    # ASSERT: Check if the returned object is an instance of GoogleService
    assert isinstance(service, GoogleService)


def test_create_service_default_is_google(monkeypatch) -> None:
    """
    Verify that `create_service` defaults to GoogleService when no name is given.
    """
    # ARRANGE
    monkeypatch.setenv("GOOGLE_API_KEY", "test_api_key")
    monkeypatch.setenv("GOOGLE_CX", "test_cx_id")

    # ACT
    service = create_service()

    # ASSERT
    assert isinstance(service, GoogleService)


def test_create_service_unknown_raises_value_error() -> None:
    """
    Verify that `create_service` raises a ValueError for an unsupported service name.

    This test ensures that the factory correctly handles requests for services
    that do not exist, preventing unexpected behavior.
    """
    # ARRANGE
    invalid_service_name: str = "bing"

    # ACT & ASSERT
    with pytest.raises(ValueError, match=f"Unknown service: {invalid_service_name}"):
        create_service(service_name=invalid_service_name)
