from opera_tosca_parser.parser.yaml.node import Node

from .constraint_clause import ConstraintClause
from .property_definition import PropertyDefinition
from ..entity import TypeEntity
from ..list import List
from ..map import Map
from ..reference import DataTypeReference


class DataType(TypeEntity):
    REFERENCE = DataTypeReference("data_types")
    ATTRS = dict(
        constraints=List(ConstraintClause),
        properties=Map(PropertyDefinition),
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize DataType object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        # Let the validator handle non-dict case
        if not isinstance(yaml_node.value, dict):
            return yaml_node

        # Make sure we have derived_from key
        for k in yaml_node.value:
            if k.value == "derived_from":
                return yaml_node

        # Create default derived_from spec if missing
        data = {Node("derived_from"): Node("None")}
        data.update(yaml_node.value)
        return Node(data, yaml_node.loc)
