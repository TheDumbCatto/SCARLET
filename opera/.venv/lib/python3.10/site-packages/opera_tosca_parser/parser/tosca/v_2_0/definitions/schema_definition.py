from __future__ import annotations

from opera_tosca_parser.parser.yaml.node import Node
from .constraint_clause import ConstraintClause
from ..entity import Entity
from ..list import List
from ..reference import DataTypeReference
from ..string import String


class SchemaDefinition(Entity):
    ATTRS = dict(
        type=DataTypeReference("data_types"),
        description=String,
        constraints=List(ConstraintClause)
    )
    REQUIRED = {"type"}

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate SchemaDefinition object
        :param yaml_node: YAML node
        """
        cls.ATTRS.update(dict(
            key_schema=SchemaDefinition,
            # TODO: Add conditions for entry_schema.
            entry_schema=SchemaDefinition,
        ))
        super().validate(yaml_node)
