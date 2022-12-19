from opera_tosca_parser.parser.yaml.node import Node

from .range import Range
from ..entity import Entity
from ..reference import Reference


class RequirementDefinition(Entity):
    ATTRS = dict(
        capability=Reference("capability_types"),
        node=Reference("node_types"),
        relationship=Reference("relationship_types"),
        occurrences=Range,
    )
    REQUIRED = {"capability"}

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize RequirementDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("capability"): yaml_node})
        return yaml_node

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate RequirementDefinition object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if "relationship" in yaml_node.bare and not isinstance(yaml_node.bare["relationship"], str):
            cls.abort("Expected a relationship type name as a 'relationship' value.", yaml_node.loc)
