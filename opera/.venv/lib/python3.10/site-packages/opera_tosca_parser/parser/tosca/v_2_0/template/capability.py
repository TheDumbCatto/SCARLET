from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.value import Value


class Capability:
    def __init__(self, name: str, properties: Dict[str, Value], attributes: Dict[str, Value]):
        """
        Construct a new Capability object
        :param name: Capability name
        :param properties: Capability properties
        :param attributes: Capability attributes
        """
        self.name = name
        self.properties = properties
        self.attributes = attributes
