from __future__ import annotations

from opera_tosca_parser.parser.tosca.v_2_0.file_uri import FileURI
from opera_tosca_parser.parser.yaml.node import Node
from ..entity import Entity
from ..string import String


class ImportDefinition(Entity):
    ATTRS = dict(
        url=FileURI,
        # TODO: Add a separate object with validation for profiles if needed.
        profile=String,
        repository=String,
        # TODO: Support namespaces.
        namespace=String
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize ImportDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Invalid import data. Expected string or dict.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("url"): yaml_node})
        return yaml_node
