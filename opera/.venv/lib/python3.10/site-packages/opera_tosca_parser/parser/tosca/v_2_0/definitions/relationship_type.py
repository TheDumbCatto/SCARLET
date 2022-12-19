from .attribute_definition import AttributeDefinition
from .definition_collector_mixin import DefinitionCollectorMixin  # type: ignore
from .interface_definition import InterfaceDefinition
from .property_definition import PropertyDefinition
from ..entity import TypeEntity
from ..list import List
from ..map import Map
from ..reference import Reference


class RelationshipType(DefinitionCollectorMixin, TypeEntity):
    REFERENCE = Reference("relationship_types")
    ATTRS = dict(
        properties=Map(PropertyDefinition),
        attributes=Map(AttributeDefinition),
        interfaces=Map(InterfaceDefinition),
        valid_capability_types=List(Reference("capability_types")),
        valid_target_node_types=List(Reference("node_types")),
        valid_source_node_types=List(Reference("node_types"))
    )
