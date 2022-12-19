from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.template.operation import Operation


class Interface:
    def __init__(self, name: str, operations: Dict[str, Operation]):
        """
        Construct a new Interface object
        :param name: Interface name
        :param operations: Interface operations
        """
        self.name = name
        self.operations = operations
