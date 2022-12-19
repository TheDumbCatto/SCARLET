from opera_tosca_parser.parser.yaml.node import Node
from .constraint_clause import ConstraintClause
from ..entity import Entity
from ..list import List


class ConditionClauseDefinition(Entity):
    ATTRS = {}
    KEYNAMES = {"and", "or", "not"}

    @classmethod
    def validate(cls, yaml_node: Node):
        """
        Validate ConditionClauseDefinition object
        :param yaml_node: YAML node
        """
        for key in yaml_node.bare:
            if key in cls.KEYNAMES:
                cls.ATTRS = {
                    "and": List(ConditionClauseDefinition),
                    "or": List(ConditionClauseDefinition),
                    "not": List(ConditionClauseDefinition),
                }
            elif key == "assert":
                cls.abort("The assert keyname is deprecated. Please use and condition clause instead.", yaml_node.loc)
            else:
                if isinstance(yaml_node.bare[key], list):
                    cls.ATTRS[key] = List(ConstraintClause)
                else:
                    cls.ATTRS[key] = ConstraintClause
        super().validate(yaml_node)
