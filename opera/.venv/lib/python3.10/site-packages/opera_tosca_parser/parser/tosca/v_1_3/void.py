from __future__ import annotations

from typing import Optional

from opera_tosca_parser.parser.tosca.v_1_3.base import Base
from opera_tosca_parser.parser.tosca.v_1_3.value import Value
from opera_tosca_parser.parser.yaml.node import Node


class Void(Base):
    """Marker for parts of the document that should be parsed after initial semantic analysis"""

    @classmethod
    def build(cls, yaml_node: Node) -> Void:
        """
        Build Void object from YAML Node
        :param yaml_node: YAML node
        :return: Void object
        """
        return cls(yaml_node)

    def __init__(self, yaml_node: Node):
        """
        Construct Void object
        :param yaml_node: YAML node
        """
        super().__init__(yaml_node.bare, yaml_node.loc)
        self.raw = yaml_node

    def get_value(self, typ: Optional) -> Value:
        """
        Get Value object from Void object
        :param typ: YAML node type
        :return: Value object
        """
        return Value(typ, True, self.data)
