from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_1_3.template.topology import Topology
    from opera_tosca_parser.parser.tosca.v_1_3.template.relationship import Relationship
    from opera_tosca_parser.parser.tosca.v_1_3.template.node import Node
    from opera_tosca_parser.parser.tosca.v_1_3.definitions.range import Range


class Requirement:
    def __init__(self, name: str, target_name: str, relationship: Relationship, occurrences: Optional[Range] = None):
        """
        Construct a new Requirement object
        :param name: Requirement name
        :param target_name: Requirement target node name
        :param relationship: Requirement relationship
        :param occurrences: Requirement occurrences
        """
        self.name = name
        self.target_name = target_name
        self.relationship = relationship
        self.occurrences = occurrences

        # This will be set when requirement gets resolved
        self.target: Optional[Node] = None

    def resolve(self, topology: Topology):
        """
        Resolve requirement (set target node and relationship topology)
        :param topology: Topology object, where requirement was inserted
        """
        self.target = topology.get_node(self.target_name)
        self.relationship.topology = topology
