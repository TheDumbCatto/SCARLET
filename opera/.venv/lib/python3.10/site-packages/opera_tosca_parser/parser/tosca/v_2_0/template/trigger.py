from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.template.node import Node
    from opera_tosca_parser.parser.tosca.v_2_0.string import String
    from opera_tosca_parser.parser.tosca.v_2_0.definitions.trigger_definition import TriggerExtendedConditionNotation


class Trigger:
    def __init__(self, name: str, event: String, target_filter: Tuple[str, Node],
                 condition: TriggerExtendedConditionNotation, action: list):
        """
        Construct a new Trigger object
        :param name: Trigger name
        :param event: Trigger event
        :param target_filter: Trigger target_filter
        :param condition: Trigger condition
        :param action: Trigger action
        """
        self.name = name
        self.event = event
        self.target_filter = target_filter
        self.condition = condition
        self.action = action
