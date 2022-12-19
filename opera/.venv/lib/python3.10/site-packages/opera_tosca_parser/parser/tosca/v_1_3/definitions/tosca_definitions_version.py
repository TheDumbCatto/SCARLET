from opera_tosca_parser.parser.yaml.node import Node
from ..string import String


class ToscaDefinitionsVersion(String):
    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate ToscaDefinitionsVersion object
        :param yaml_node: YAML node
        """
        super().validate(yaml_node)
        if yaml_node.value != "tosca_simple_yaml_1_3":
            cls.abort(f"Invalid TOSCA version: {yaml_node.value}. Expected tosca_simple_yaml_1_3.", yaml_node.loc)
