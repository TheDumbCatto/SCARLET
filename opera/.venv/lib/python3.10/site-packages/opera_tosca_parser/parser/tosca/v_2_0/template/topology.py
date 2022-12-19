from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.template.node import Node
    from opera_tosca_parser.parser.tosca.v_2_0.template.policy import Policy
    from opera_tosca_parser.parser.tosca.v_2_0.template.relationship import Relationship
    from opera_tosca_parser.parser.tosca.v_2_0.value import Value


class Topology:
    def __init__(self, inputs: Dict[str, Value], outputs: Dict[str, Value], nodes: Dict[str, Node],
                 relationships: Dict[str, Relationship], policies: List[Policy]):
        """
        Construct a new topology object
        :param inputs: Topology inputs
        :param outputs: Topology outputs
        :param nodes: Topology nodes
        :param relationships: Topology relationships
        :param policies: Topology policies
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = nodes
        self.relationships = relationships
        self.policies = policies

        for node in self.nodes.values():
            node.topology = self

    def get_node(self, name: str) -> Node:
        """
        Get node by name from topology
        :param name: The name of node
        :return: Node object
        """
        return self.nodes[name]

    def resolve_requirements(self):
        """
        Resolve requirements from topology nodes
        """
        for node in self.nodes.values():
            node.resolve_requirements(self)
        self.resolve_relationships()

    def resolve_relationships(self):
        """
        Resolve relationships for topology node requirements
        """
        for node in self.nodes.values():
            for req in node.requirements:
                relationship = req.relationship
                if relationship.name in self.relationships.keys():
                    self.relationships[relationship.name] = relationship

    def resolve_policies(self):
        """
        Resolve policies from topology and apply them to nodes
        """
        for node in self.nodes.values():
            for policy in self.policies:
                if policy.targets:
                    # apply policy to node if node name matches the target names that policy is limited to
                    if node.name in policy.targets.keys():
                        node.policies.append(policy)
                else:
                    # if we don't have target limits or filters apply policy to every node
                    node.policies.append(policy)
