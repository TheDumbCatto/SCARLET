from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Dict, List, Tuple, Optional, Any

from opera_tosca_parser.error import DataError

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.template.topology import Topology
    from opera_tosca_parser.parser.tosca.v_2_0.template.policy import Policy
    from opera_tosca_parser.parser.tosca.v_2_0.template.capability import Capability
    from opera_tosca_parser.parser.tosca.v_2_0.template.interface import Interface
    from opera_tosca_parser.parser.tosca.v_2_0.template.requirement import Requirement
    from opera_tosca_parser.parser.tosca.v_2_0.value import Value


class Node:
    def __init__(self, name: str, types: Tuple[str, ...], properties: Dict[str, Value], attributes: Dict[str, Value],
                 requirements: List[Requirement], capabilities: List[Capability], interfaces: Dict[str, Interface],
                 artifacts: Dict[str, Value]):
        """
        Construct a new Node object
        :param name: Node name
        :param types: Node types for derivation
        :param properties: Node properties
        :param attributes: Node attributes
        :param requirements: Node requirements
        :param capabilities: Node capabilities
        :param interfaces: Node interfaces
        :param artifacts: Node artifacts
        """
        self.name = name
        self.types = types
        self.properties = properties
        self.attributes = attributes
        self.requirements = requirements
        self.capabilities = capabilities
        self.interfaces = interfaces
        self.artifacts = artifacts

        # This will be set when the connected policies are resolved in topology.
        self.policies: List[Policy] = []
        # This will be set when the node is inserted into a topology.
        self.topology: Optional[Topology] = None
        # This will be set at instantiation time.
        self._instance = None  # type: ignore

    def resolve_requirements(self, topology: Topology):
        """
        Resolve node requirements
        :param topology: Topology object, where node was inserted
        """
        requirement_count = Counter([r.name for r in self.requirements])
        for r in self.requirements:
            count_range = r.count_range.data if r.count_range else None
            min_occurrences = count_range[0] if count_range else 1
            max_occurrences = count_range[1] if count_range else 1

            if requirement_count[r.name] < min_occurrences:
                raise DataError(
                    f"Not enough occurrences found for requirement '{r.name}'. Minimum is: {min_occurrences}."
                )
            if requirement_count[r.name] > max_occurrences:
                raise DataError(
                    f"Too many occurrences found for requirement '{r.name}'. Maximum is: {max_occurrences}."
                )
            r.resolve(topology)

    def is_a(self, typ: str) -> bool:
        """
        Check whether a node is of certain type
        :param typ: Node type
        """
        return typ in self.types

    @property
    def instance(self) -> Any:
        """
        Get instance for this node template
        Raise error if not instantiated
        :return: Instance
        """
        if not self._instance:
            raise DataError(f"Node template {self.name} was not instantiated yet.")
        return self._instance

    @instance.setter
    def instance(self, value: Any):
        """
        Set instance for this node template
        :param value: Instance
        """
        self._instance = value
