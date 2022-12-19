from typing import Tuple, Any, Iterator

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.tosca.v_1_3.base import Base
from opera_tosca_parser.parser.yaml.node import Node


class ListWrapper(Base):
    def __getitem__(self, index: int) -> Any:
        """
        Get Integer item
        :param index: Index
        :return: Item
        """
        return self.data[index]

    def __iter__(self) -> Iterator:
        """
        Get iterator for ListWrapper
        :return: Iterator
        """
        return iter(self.data)

    def dig(self, key: str, *subpath: Tuple[str, ...]) -> Any:
        """
        Dig into ListWrapper object
        :param key: Key
        :param subpath: Subpath tuple
        :return: Digged data
        """
        try:
            item = self.data[key]
        except (IndexError, TypeError):
            return None
        return item.dig(*subpath) if subpath else item

    def visit(self, method: str, *args, **kwargs):
        """
        Visit ListWrapper object
        :param method: Method
        """
        for v in self:
            v.visit(method, *args, **kwargs)


class List:
    def __init__(self, value_class: Any):
        """
        Construct List object
        :param value_class: Value class
        """
        self.value_class = value_class

    def parse(self, yaml_node: Node) -> ListWrapper:
        """
        Parse YAML Node to List object
        :param yaml_node: YAML node
        :return: ListWrapper object
        """
        if not isinstance(yaml_node.value, list):
            raise ParseError("Expected list.", yaml_node.loc)

        return ListWrapper([self.value_class.parse(v) for v in yaml_node.value], yaml_node.loc)
