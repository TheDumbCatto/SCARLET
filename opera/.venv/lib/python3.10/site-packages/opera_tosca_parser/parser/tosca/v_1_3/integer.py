from opera_tosca_parser.parser.yaml.node import Node
from .comparable import Comparable


class Integer(Comparable):
    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate Integer object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if not isinstance(yaml_node.value, int) or isinstance(yaml_node.value, bool):
            cls.abort("Expected integer.", yaml_node.loc)
