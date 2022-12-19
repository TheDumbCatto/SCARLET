from __future__ import annotations

from typing import Any, Optional
from typing import Set, Dict, Type, Union

from opera_tosca_parser.parser.yaml.node import Node
from .base import Base
from .list import List
from .map import Map, MapWrapper
from .reference import Reference, ReferenceXOR
from .string import String
from .version import Version


class Entity(MapWrapper):
    # This must be overridden in derived classes
    ATTRS: Dict[str, Union[Type[Base], Base, Map, List, Reference, ReferenceXOR]] = {}

    # This can be overridden in derived classes
    REQUIRED: Set[str] = set()

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate Entity object
        :param yaml_node: YAML node
        """
        if cls.ATTRS == {}:
            raise AssertionError()
        if not isinstance(cls.REQUIRED, set):
            raise AssertionError()

        if not isinstance(yaml_node.value, dict):
            cls.abort("Expected map.", yaml_node.loc)

        data_keys = set()
        for k in yaml_node.value:
            if not isinstance(k.value, str):
                cls.abort("Expected string", k.loc)
            data_keys.add(k.value)

        missing_keys = cls.REQUIRED - data_keys
        if missing_keys:
            cls.abort(f"Missing required keynames: {', '.join(missing_keys)}", yaml_node.loc)

        extra_keys = data_keys - cls.attrs().keys()
        if extra_keys:
            cls.abort(f"Invalid keys: {', '.join(extra_keys)}", yaml_node.loc)

    @classmethod
    def build(cls, yaml_node: Node) -> Entity:
        """
        Build Base object from YAML node
        :param yaml_node: YAML node
        :return: Entity object
        """
        classes = cls.attrs()
        data = {
            k.value: classes[k.value].parse(v)
            for k, v in yaml_node.value.items()
        }
        return cls(data, yaml_node.loc)

    @classmethod
    def attrs(cls) -> dict:
        """
        Retrieve attributes
        :return: Dict of attributes
        """
        return cls.ATTRS

    def __getattr__(self, key: str) -> Any:
        """
        Retrieve attribute
        :param key:Attribute key
        :return: Attribute
        """
        try:
            return self.data[key]
        except KeyError as e:
            raise AttributeError(key) from e


class TypeEntity(Entity):
    REFERENCE: Optional[Reference] = None  # Override in subclasses

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize DataType object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        # Let the validator handle non-dict case
        if not isinstance(yaml_node.value, dict):
            return yaml_node

        # Make sure we have derived_from key
        for k in yaml_node.value:
            if k.value == "derived_from":
                return yaml_node

        # Create default derived_from spec if missing
        data = {Node("derived_from"): Node("None")}
        data.update(yaml_node.value)
        return Node(data, yaml_node.loc)

    @classmethod
    def validate(cls, yaml_node) -> None:
        """
        Validate TypeEntity object
        :param yaml_node: YAML node
        :return: NoneType object
        """
        super().validate(yaml_node)
        for key in yaml_node.value:
            if key.value == "derived_from":
                return

    @classmethod
    def attrs(cls) -> dict:
        """
        Retrieve attributes
        :return: Dict of attributes
        """
        if not isinstance(cls.REFERENCE, Reference):
            raise AssertionError(f"Override REFERENCE in {cls.__name__} with Reference.")

        attributes = cls.ATTRS.copy()
        attributes.update(
            derived_from=cls.REFERENCE,
            description=String,
            metadata=Map(String),
            version=Version,
        )
        return attributes
