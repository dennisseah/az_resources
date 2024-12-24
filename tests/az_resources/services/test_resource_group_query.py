from unittest.mock import AsyncMock, MagicMock

import pytest
from azure.mgmt.resourcegraph.models import QueryResponse

from az_resources.services.resource_group_query import (
    ResourceGroupQuery,
    ResourceGroupQueryEnv,
)


@pytest.fixture
def mock_client():
    return_value = MagicMock(spec=QueryResponse)
    return_value.total_records = 2
    return_value.data = [
        {
            "id": "id",
            "name": "name",
            "type": "type",
            "tenantId": "tenantId",
            "kind": "kind",
            "location": "location",
            "resourceGroup": "resourceGroup",
            "subscriptionId": "subscriptionId",
            "managedBy": "managedBy",
            "plan": {"plan": "plan"},
            "properties": {"properties": "properties"},
        }
    ]

    client = MagicMock()
    client.resources = AsyncMock(return_value=return_value)
    client.close = AsyncMock()
    return client


def test_get_az_graph_client():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    assert svc.get_az_graph_client() is not None


@pytest.mark.asyncio
async def test_query(mock_client):
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.get_az_graph_client = MagicMock(return_value=mock_client)

    resources = await svc.query("query")
    assert len(resources) == 1


@pytest.mark.asyncio
async def test_list_all():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.query = AsyncMock(return_value=[1])

    resources = await svc.list_all()
    assert len(resources) == 1


@pytest.mark.asyncio
async def test_fetch_resources():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.query = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_resources("test")
    assert len(resources) == 2


@pytest.mark.asyncio
async def test_fetch_changes_to_resource_group():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.query = AsyncMock(return_value=[1, 2])

    resources = await svc.fetch_changes_to_resource_group("test")
    assert len(resources) == 2
