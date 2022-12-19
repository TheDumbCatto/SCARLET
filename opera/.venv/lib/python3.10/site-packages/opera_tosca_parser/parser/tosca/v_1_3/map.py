from __future__ import annotations

import collections
from typing import Tuple, Any, Iterator, ValuesView, KeysView, ItemsView, Optional

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser.yaml.node import Node
from .base import Base


class MapWrapper(Base):
    def __getitem__(self, key: str) -> Any:
        """
        Get MapWrapper item
        :param key: Key
        :return: Item
        """
        return self.data[key]

    def __iter__(self) -> Iterator:
        """
        Get iterator for MapWrapper
        :return: Iterator
        """
        return iter(self.data)

    def values(self) -> ValuesView:
        """
        Get values for MapWrapper
        :return: Values
        """
        return self.data.values()

    def keys(self) -> KeysView:
        """
        Get keys for v
        :return: Keys
        """
        return self.data.keys()

    def items(self) -> ItemsView:
        """
        Get items for MapWrapper
        :return: Items
        """
        return self.data.items()

    def get(self, key: str, default: Optional[Any] = None) -> Optional[dict]:
        """
        Get item for MapWrapper
        :param key: Key
        :param default: Default value
        :return: Item or None
        """
        return self.data.get(key, default)

    def dig(self, key: str, *subpath: Tuple[str, ...]) -> Any:
        """
        Dig into ListWrapper object
        :param key: Key
        :param subpath: Subpath tuple
        :return: Digged data
        """
        if key not in self.data:
            return None
        if not subpath:
            return self.data[key]
        return self.data[key].dig(*subpath)

    def merge(self, other: MapWrapper):
        """
        Merge with other MapWrapper object
        :param other: MapWrapper object to merge with
        """
        duplicates = set(self.keys()) & set(other.keys())
        if duplicates:
            self.abort(f"Duplicate keys '{', '.join(duplicates)}' found in {self.loc} and {other.loc}",
                       self.loc)
        self.data.update(other.data)

    def visit(self, method: str, *args, **kwargs):
        """
        Visit MapWrapper object
        :param method: Method
        """
        for v in self.values():
            v.visit(method, *args, **kwargs)


class Map:
    def __init__(self, value_class: Any):
        """
        Construct Map object
        :param value_class: Value class
        """
        self.value_class = value_class

    def parse(self, yaml_node: Node) -> MapWrapper:
        """
        Parse YAML Node to Map object
        :param yaml_node: YAML node
        :return: MapWrapper object
        """
        if not isinstance(yaml_node.value, dict):
            raise ParseError("Expected map.", yaml_node.loc)

        for k in yaml_node.value:
            if not isinstance(k.value, str):
                ParseError("Expected string key.", k.loc)

        return MapWrapper(collections.OrderedDict(
            (k.value, self.value_class.parse(v))
            for k, v in yaml_node.value.items()
        ), yaml_node.loc)


class OrderedMap(Map):
    def parse(self, yaml_node: Node) -> MapWrapper:
        """
        Parse YAML Node to OrderedMap object
        :param yaml_node: YAML node
        :return: MapWrapper object
        """
        if not isinstance(yaml_node.value, list):
            raise ParseError("Expected list of single-key maps.", yaml_node.loc)

        data = collections.OrderedDict()
        for item in yaml_node.value:
            if not isinstance(item.value, dict) or len(item.value) != 1:
                raise ParseError("Expected single-key map.", item.loc)
            (k, v), = item.value.items()
            data[k] = v
        return super().parse(Node(data, yaml_node.loc))
