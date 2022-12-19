from opera_tosca_parser.parser.yaml.node import Node
from .node_filter_definition import NodeFilterDefinition
from ..bool import Bool
from ..entity import Entity
from ..integer import Integer
from ..list import List
from ..map import Map
from ..reference import Reference
from ..string import String
from ..void import Void


class RequirementAssignment(Entity):
    ATTRS = dict(
        capability=String,
        node=Reference("topology_template", "node_templates"),
        relationship=Reference("topology_template", "relationship_templates"),
        allocation=Map(Void),
        node_filter=NodeFilterDefinition,
        count=Integer,
        directives=List(String),
        optional=Bool
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize RequirementAssignment object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("node"): yaml_node})
        return yaml_node

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate RequirementAssignment object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if "relationship" in yaml_node.bare and not isinstance(yaml_node.bare["relationship"], str):
            cls.abort("Expected a relationship template name as a 'relationship' value.", yaml_node.loc)
        if "count" in yaml_node.bare and isinstance(yaml_node.bare["count"], int) and yaml_node.bare["count"] < 0:
            cls.abort(
                f"The count keyname value should be non-negative integer, received: {yaml_node.bare['count']}",
                yaml_node.loc
            )
        if "directives" in yaml_node.bare and not isinstance(yaml_node.bare["directives"], list):
            cls.abort("Expected directives keyname as a list of strings.", yaml_node.loc)
        if "directives" in yaml_node.bare and isinstance(yaml_node.bare["directives"], list):
            for directive in yaml_node.bare["directives"]:
                valid_directives = ("internal", "external")
                if directive not in valid_directives:
                    cls.abort(f"The directive keyname should be one of: {', '.join(valid_directives)}.", yaml_node.loc)
