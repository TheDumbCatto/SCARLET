from .constraint_clause import ConstraintClause
from .property_definition import PropertyDefinition
from .schema_definition import SchemaDefinition
from ..entity import TypeEntity
from ..list import List
from ..map import Map
from ..reference import DataTypeReference


class DataType(TypeEntity):
    REFERENCE = DataTypeReference("data_types")
    ATTRS = dict(
        constraints=List(ConstraintClause),
        properties=Map(PropertyDefinition),
        key_schema=SchemaDefinition,
        # TODO: Add conditions for entry_schema.
        entry_schema=SchemaDefinition
    )
