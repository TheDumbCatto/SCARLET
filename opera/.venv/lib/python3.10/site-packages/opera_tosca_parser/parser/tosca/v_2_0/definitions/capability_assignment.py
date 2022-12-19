from opera_tosca_parser.parser.yaml.node import Node
from ..entity import Entity
from ..list import List
from ..map import Map
from ..string import String
from ..void import Void


class CapabilityAssignment(Entity):
    ATTRS = dict(
        properties=Map(Void),
        attributes=Map(Void),
        directives=List(String)
    )

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate RequirementDefinition object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if "directives" in yaml_node.bare and not isinstance(yaml_node.bare["directives"], list):
            cls.abort("Expected directives keyname as a list of strings.", yaml_node.loc)
        if "directives" in yaml_node.bare and isinstance(yaml_node.bare["directives"], list):
            for directive in yaml_node.bare["directives"]:
                valid_directives = ("internal", "external")
                if directive not in valid_directives:
                    cls.abort(f"The directive keyname should be one of: {', '.join(valid_directives)}.", yaml_node.loc)
