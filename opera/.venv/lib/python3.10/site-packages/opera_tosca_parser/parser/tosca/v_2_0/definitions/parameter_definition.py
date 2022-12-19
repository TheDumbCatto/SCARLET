from typing import Dict, Any, Optional

from opera_tosca_parser.parser.tosca.v_2_0.value import Value
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


# TODO: See if we can unify ParameterDefinition and PropertyDefinition.
class ParameterDefinition(Entity):
    ATTRS = dict(
        type=DataTypeReference("data_types"),
        description=String,
        required=Bool,
        default=Void,
        value=Void,
        status=Status,
        constraints=List(ConstraintClause),
        key_schema=SchemaDefinition,
        # TODO: Add conditions for entry_schema.
        entry_schema=SchemaDefinition,
        external_schema=String,
        metadata=Map(String),
        # TODO: Support attribute selection format with mapping.
        mapping=Void
    )

    def get_value(self, typ: Optional) -> Value:
        """
        Get Value object from ParameterDefinition object
        :param typ: YAML node type
        :return: Value object
        """
        if "value" in self and "mapping" in self:
            self.abort("The value and mapping keynames are mutually exclusive.", self.loc)
        if "value" in self:
            return self.value.get_value(typ)
        if "default" in self:
            return self.default.get_value(typ)
        return Value(typ, False)

    def get_value_type(self, service_ast: Dict[str, Any]) -> None:  # pylint: disable=no-self-use
        """
        Get Value type for ParameterDefinition object
        :param service_ast: Abstract syntax tree dict
        :return: None
        """
        # TODO: Implement type checks.
        return None
