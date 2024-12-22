from typing import Protocol

from az_resources.models.resource import Resource


class IResourceGroupQuery(Protocol):
    def list_all(self) -> list[Resource]: ...

    def fetch_resources(self, resource_group_name: str) -> list[Resource]: ...
