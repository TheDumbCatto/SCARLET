from opera_tosca_parser.parser.yaml.node import Node

from .artifact_definition import ArtifactDefinition
from ..entity import Entity
from ..list import List


class NotificationImplementationDefinition(Entity):
    ATTRS = dict(
        primary=ArtifactDefinition,
        dependencies=List(ArtifactDefinition),
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize NotificationImplementationDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("primary"): yaml_node})
        return yaml_node
