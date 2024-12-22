from typing import Any

from pydantic import BaseModel


class Resource(BaseModel):
    id: str
    name: str
    type: str
    tenantId: str
    kind: str
    location: str
    resourceGroup: str
    subscriptionId: str
    managedBy: str
    plan: dict[str, Any] | None
    properties: dict[str, Any]
    sku: dict[str, Any] | None = None
    tags: dict[str, Any] | None = None
    identity: dict[str, Any] | None = None
    zones: list[str] | None = None
