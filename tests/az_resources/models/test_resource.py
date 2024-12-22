from az_resources.models.resource import Resource


def test_init_with_defaults():
    Resource(
        id="id",
        name="name",
        type="type",
        tenantId="tenantId",
        kind="kind",
        location="location",
        resourceGroup="resourceGroup",
        subscriptionId="subscriptionId",
        managedBy="managedBy",
        plan={"plan": "plan"},
        properties={"properties": "properties"},
    )
