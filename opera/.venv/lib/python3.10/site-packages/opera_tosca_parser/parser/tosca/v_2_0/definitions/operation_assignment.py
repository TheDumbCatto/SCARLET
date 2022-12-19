from opera_tosca_parser.parser.yaml.node import Node

from .operation_implementation_definition import OperationImplementationDefinition
from ..entity import Entity
from ..list import List
from ..map import Map
from ..string import String
from ..void import Void


class OperationAssignment(Entity):
    ATTRS = dict(
        implementation=OperationImplementationDefinition,
        inputs=Map(Void),
        outputs=Map(List(String)),
    )

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize OperationDefinitionForTemplate object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("implementation"): yaml_node})
        return yaml_node
