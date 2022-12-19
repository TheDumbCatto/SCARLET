from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.value import Value
    from opera_tosca_parser.parser.tosca.v_2_0.template.trigger import Trigger


class Policy:
    def __init__(self, name: str, types: Tuple[str, ...], properties: Dict[str, Value], targets: Dict[str, Value],
                 triggers: Dict[str, Trigger]):
        """
        Construct a new Policy object
        :param name: Policy name
        :param types: Policy types for derivation
        :param properties: Policy properties
        :param targets: Policy targets
        :param triggers: Policy triggers
        """
        self.name = name
        self.types = types
        self.properties = properties
        self.targets = targets
        self.triggers = triggers
