from typing import Dict, Any, Optional

from opera_tosca_parser.parser.tosca.v_1_3.value import Value
from .constraint_clause import ConstraintClause
from .schema_definition import SchemaDefinition
from .status import Status
from ..bool import Bool
from ..entity import Entity
from ..list import List
from ..map import Map
from ..reference import DataTypeReference
from ..string import String
from ..void import Void


class PropertyDefinition(Entity):
    ATTRS = dict(
        type=DataTypeReference("data_types"),
        description=String,
        required=Bool,
        default=Void,
        status=Status,
        constraints=List(ConstraintClause),
        key_schema=SchemaDefinition,
        entry_schema=SchemaDefinition,
        external_schema=String,
        metadata=Map(String),
    )
    REQUIRED = {"type"}

    def get_value(self, typ: Optional) -> Value:
        """
        Get Value object from PropertyDefinition object
        :param typ: YAML node type
        :return: Value object
        """
        if "value" in self:
            return self.value.get_value(typ)
        if "default" in self:
            return self.default.get_value(typ)
        return Value(typ, False)

    def get_value_type(self, service_ast: Dict[str, Any]) -> None:  # pylint: disable=no-self-use
        """
        Get Value type for ActivityDefinition object
        :param service_ast: Abstract syntax tree dict
        :return: None
        """
        # TODO: Implement types later.
        return None
