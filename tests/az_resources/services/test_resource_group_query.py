from unittest.mock import MagicMock

import pytest
from azure.mgmt.resourcegraph.models import QueryResponse
from pytest_mock import MockerFixture

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
    client.resources = MagicMock(return_value=return_value)
    return client


def test_get_az_graph_client(mocker: MockerFixture):
    mock_client = mocker.patch(
        "az_resources.services.resource_group_query.ResourceGraphClient"
    )

    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    assert svc.get_az_graph_client() is not None
    assert svc.get_az_graph_client() is not None
    mock_client.assert_called_once()  # only called once


def test_query(mock_client):
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.get_az_graph_client = MagicMock(return_value=mock_client)

    resources = svc.query("query")
    assert len(resources) == 1


def test_list_all():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.query = MagicMock(return_value=[1])

    resources = svc.list_all()
    assert len(resources) == 1


def test_fetch_resources():
    svc = ResourceGroupQuery(env=ResourceGroupQueryEnv(azure_subscription_id="test"))
    svc.query = MagicMock(return_value=[1, 2])

    resources = svc.fetch_resources("test")
    assert len(resources) == 2
