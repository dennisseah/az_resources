import json
import os

from az_resources.hosting import container
from az_resources.protocols.i_resource_group_query import IResourceGroupQuery


def main():
    svc = container[IResourceGroupQuery]

    # get all resource groups in the subscription
    # subscruption_id is in .env file
    all_resource_groups = svc.list_all()
    with open(os.path.join("outputs", "resource_group.json"), "w") as f:
        json.dump([rg.model_dump() for rg in all_resource_groups], f, indent=2)

    # list all resources in the first resource group
    if len(all_resource_groups) > 0:
        resources = svc.fetch_resources(all_resource_groups[0].name)
        with open(os.path.join("outputs", "resources.json"), "w") as f:
            json.dump([r.model_dump() for r in resources], f, indent=2)

        # list all changes to the first resource group
        changes = svc.fetch_changes_to_resource_group(all_resource_groups[0].name)
        with open(os.path.join("outputs", "changes.json"), "w") as f:
            json.dump([r.model_dump() for r in changes], f, indent=2)


if __name__ == "__main__":
    main()
