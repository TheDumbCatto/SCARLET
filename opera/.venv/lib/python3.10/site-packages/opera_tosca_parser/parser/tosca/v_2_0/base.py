from __future__ import annotations

from typing import Any, Optional

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.utils.location import Location
from opera_tosca_parser.parser.yaml.node import Node


class Base:
    @classmethod
    def parse(cls, yaml_node: Node) -> Base:
        """
        Parse YAML Node to Base object
        :param yaml_node: YAML node
        :return: Parsed object
        """
        yaml_node = cls.normalize(yaml_node)
        cls.validate(yaml_node)
        return cls.build(yaml_node)

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize Base object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        return yaml_node

    @classmethod
    def validate(cls, _yaml_node: Node):
        """
        Validate Base object
        :param _yaml_node: YAML node
        """
        pass

    @classmethod
    def build(cls, yaml_node: Node) -> Base:
        """
        Build Base object from YAML node
        :param yaml_node: YAML node
        :return: Base object
        """
        return cls(yaml_node.bare, yaml_node.loc)

    @classmethod
    def abort(cls, msg: str, loc: Optional[Location] = None):
        """
        Abort from Base class
        :param msg: Error message
        :param loc: Location of the error in TOSCA template
        :raises: ParseError
        """
        raise ParseError(f"[{cls.__name__}] {msg}", loc)

    def __init__(self, data: Any, loc: Optional[Location]):
        """
        Construct Base object
        :param data: Data
        :param loc: Location object
        """
        self.data = data
        self.loc = loc

    def __str__(self) -> str:
        """Overridden string representation"""
        return str(self.data)

    def visit(self, method: str, *args, **kwargs):
        """
        Visit Base object
        :param method: Method
        """
        if hasattr(self, method):
            getattr(self, method)(*args, **kwargs)
