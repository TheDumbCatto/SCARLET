from opera_tosca_parser.parser.yaml.node import Node
from ..string import String


class Status(String):
    VALID_STATES = {"supported", "unsupported", "experimental", "deprecated"}

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate Status object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if yaml_node.value not in cls.VALID_STATES:
            cls.abort(f"Invalid state: '{yaml_node.value}'.", yaml_node.loc)
