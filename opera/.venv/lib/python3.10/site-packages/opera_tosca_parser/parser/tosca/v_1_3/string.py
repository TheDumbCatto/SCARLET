from opera_tosca_parser.parser.yaml.node import Node
from .comparable import Comparable


class String(Comparable):
    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate String object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if not isinstance(yaml_node.value, str):
            cls.abort("Expected string input", yaml_node.loc)
