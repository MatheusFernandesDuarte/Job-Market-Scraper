# src/core/factories/service_factory.py

"""
Factory module for creating instances of search service providers.
"""

from src.services.google.service import GoogleService


def create_service(service_name: str = "google") -> GoogleService:
    """
    Create and return an instance of a specified search service.

    This factory pattern allows for easy extension to support other
    search providers in the future.

    Args:
        service_name (str): The name of the service to create.
            Currently, only "google" is supported. Defaults to "google".

    Returns:
        GoogleService: An initialized instance of the requested service provider.

    Raises:
        ValueError: If the requested service_name is not supported.
    """
    if service_name.lower() == "google":
        service_instance: GoogleService = GoogleService()
        return service_instance
    raise ValueError(f"Unknown service: {service_name}")
