from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest, QueryRequestOptions
from lagom.environment import Env

from az_resources.models.resource import Resource
from az_resources.protocols.i_resource_group_query import IResourceGroupQuery


class ResourceGroupQueryEnv(Env):
    azure_subscription_id: str


@dataclass
class ResourceGroupQuery(IResourceGroupQuery):
    env: ResourceGroupQueryEnv
    az_graph_client: ResourceGraphClient | None = None

    def get_az_graph_client(self):
        if self.az_graph_client:
            return self.az_graph_client

        self.az_graph_client = ResourceGraphClient(DefaultAzureCredential())
        return self.az_graph_client

    def query(self, query: str) -> list[Resource]:
        argQuery = QueryRequest(  # type: ignore
            subscriptions=[self.env.azure_subscription_id],
            query=query,
            options=QueryRequestOptions(result_format="objectArray"),  # type: ignore
        )

        argResults = self.get_az_graph_client().resources(argQuery)
        return [Resource(**r) for r in argResults.data]  # type: ignore

    def list_all(self) -> list[Resource]:
        return self.query(
            """resourcecontainers
            |
            where type =~ 'microsoft.resources/subscriptions/resourcegroups'
            """
        )

    def fetch_resources(self, resource_group_name: str) -> list[Resource]:
        return self.query(f"Resources | where resourceGroup =~ '{resource_group_name}'")
