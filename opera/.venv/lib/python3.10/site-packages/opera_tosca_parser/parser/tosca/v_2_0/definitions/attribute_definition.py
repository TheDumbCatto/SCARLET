from typing import Optional, Dict, Any

from opera_tosca_parser.parser.tosca.v_2_0.value import Value
from .constraint_clause import ConstraintClause
from .schema_definition import SchemaDefinition
from .status import Status
from ..entity import Entity
from ..list import List
from ..map import Map
from ..reference import DataTypeReference
from ..string import String
from ..void import Void


class AttributeDefinition(Entity):
    ATTRS = dict(
        type=DataTypeReference("data_types"),
        description=String,
        default=Void,
        status=Status,
        constraints=List(ConstraintClause),
        key_schema=SchemaDefinition,
        # TODO: Add conditions for entry_schema.
        entry_schema=SchemaDefinition,
        metadata=Map(String)
    )
    REQUIRED = {"type"}

    def get_value(self, typ: Optional) -> Value:
        """
        Get Value object from AttributeDefinition object
        :param typ: YAML node type
        :return: Value object
        """
        if "default" in self:
            return self.default.get_value(typ)
        return Value(typ, False)

    def get_value_type(self, service_ast: Dict[str, Any]) -> None:  # pylint: disable=no-self-use
        """
        Get Value type for AttributeDefinition object
        :param service_ast: Abstract syntax tree dict
        :return: None
        """
        # TODO: Implement type checks later.
        return None
