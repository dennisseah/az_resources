"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging
import os

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from az_resources.protocols.i_resource_group_query import IResourceGroupQuery

load_dotenv(dotenv_path=".env")


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def logger() -> logging.Logger:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    logging.Formatter(fmt=" %(name)s :: %(levelname)-8s :: %(message)s")
    return logging.getLogger("eval_user_profiles")


@dependency_definition(container, singleton=True)
def resource_group_query() -> IResourceGroupQuery:
    from az_resources.services.resource_group_query import ResourceGroupQuery

    return container[ResourceGroupQuery]
