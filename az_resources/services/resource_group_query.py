from dataclasses import dataclass
from typing import Any

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resourcegraph.aio import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest, QueryRequestOptions
from lagom.environment import Env

from az_resources.models.resource import Resource
from az_resources.protocols.i_resource_group_query import IResourceGroupQuery


class ResourceGroupQueryEnv(Env):
    azure_subscription_id: str


@dataclass
class ResourceGroupQuery(IResourceGroupQuery):
    env: ResourceGroupQueryEnv

    def get_az_graph_client(self) -> ResourceGraphClient:
        return ResourceGraphClient(DefaultAzureCredential())

    async def query(self, query: str) -> list[Resource]:
        data: list[dict[str, Any]] = []
        argQuery = QueryRequest(
            subscriptions=[self.env.azure_subscription_id],
            query=query,
            options=QueryRequestOptions(top=100, result_format="objectArray"),
        )

        client = self.get_az_graph_client()
        try:
            argResults = await client.resources(argQuery)
            data = data + argResults.data  # type: ignore
            total = argResults.total_records

            while total != len(data):
                argQuery.options.skip = len(data)  # type: ignore
                argResults = await client.resources(argQuery)
                data = data + argResults.data  # type: ignore

            return [Resource(**r) for r in argResults.data]  # type: ignore
        finally:
            await client.close()

    async def list_all(self) -> list[Resource]:
        return await self.query(
            """resourcecontainers
            |
            where type =~ 'microsoft.resources/subscriptions/resourcegroups'
            | sort by name
            """
        )

    async def fetch_resources(self, resource_group_name: str) -> list[Resource]:
        return await self.query(
            f"""
            Resources |
                where resourceGroup =~ '{resource_group_name}'
                | sort by name
            """
        )

    async def fetch_changes_to_resource_group(
        self, resource_group_name: str
    ) -> list[Resource]:
        return await self.query(
            f"""
            resourcechanges |
                where resourceGroup =~ '{resource_group_name}'
            """
        )
