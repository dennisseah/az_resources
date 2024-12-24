from typing import Protocol

from az_resources.models.resource import Resource


class IResourceGroupQuery(Protocol):
    async def list_all(self) -> list[Resource]:
        """
        List all resource groups in the subscription.

        :return: A list of resource groups.
        """
        ...

    async def fetch_resources(self, resource_group_name: str) -> list[Resource]:
        """
        Fetch all resources in a resource group.

        :param resource_group_name: The name of the resource group.
        :return: A list of resources in the resource group.
        """
        ...

    async def fetch_changes_to_resource_group(
        self, resource_group_name: str
    ) -> list[Resource]:
        """
        Fetch all resources that have changed in a resource group.

        :param resource_group_name: The name of the resource group.
        :return: A list of resources that have changed.
        """
        ...
