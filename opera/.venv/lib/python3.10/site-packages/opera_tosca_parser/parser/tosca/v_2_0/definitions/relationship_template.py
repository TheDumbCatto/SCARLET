from typing import Dict, Any

from opera_tosca_parser.parser.tosca.v_2_0.template.relationship import Relationship
from .collector_mixin import CollectorMixin  # type: ignore
from .interface_assignment import InterfaceAssignment
from ..entity import Entity
from ..map import Map
from ..reference import Reference
from ..string import String
from ..void import Void


class RelationshipTemplate(CollectorMixin, Entity):
    ATTRS = dict(
        type=Reference("relationship_types"),
        description=String,
        metadata=Map(String),
        properties=Map(Void),
        attributes=Map(Void),
        interfaces=Map(InterfaceAssignment),
        copy=Reference("topology_template", "relationship_templates"),
    )
    REQUIRED = {"type"}

    def get_template(self, name: str, service_ast: Dict[str, Any]) -> Relationship:
        """
        Get Relationship object from template
        :param name: Relationship name
        :param service_ast: Abstract syntax tree dict
        :return: Relationship object
        """
        return Relationship(
            name=name,
            types=self.collect_types(service_ast),
            properties=self.collect_properties(service_ast),
            attributes=self.collect_attributes(service_ast),
            interfaces=self.collect_interfaces(service_ast),
        )
