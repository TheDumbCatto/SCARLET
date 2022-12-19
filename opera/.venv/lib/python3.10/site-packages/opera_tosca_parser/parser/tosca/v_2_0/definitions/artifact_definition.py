from typing import Optional, Dict, Any

import yaml

from opera_tosca_parser.parser.tosca.v_2_0.value import Value
from opera_tosca_parser.parser.yaml.node import Node
from ..entity import Entity
from ..map import Map
from ..path import Path
from ..reference import Reference
from ..string import String
from ..version import Version
from ..void import Void


class ArtifactDefinition(Entity):
    ATTRS = dict(
        type=Reference("artifact_types"),
        file=Path,
        repository=Reference("repositories"),
        description=String,
        deploy_path=String,
        artifact_version=Version,
        checksum=String,
        checksum_algorithm=String,
        properties=Map(Void),
    )
    REQUIRED = {"type", "file"}

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize ArtifactDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Expected string or map.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({
                Node("type"): Node("File"),
                Node("file"): yaml_node,
            })
        return yaml_node

    def get_value(self, typ: Optional) -> Value:
        """
        Get Value object from ArtifactDefinition object
        :param typ: YAML node type
        :return: Value object
        """
        if "file" in self:
            yaml_data = yaml.safe_load(str(self.file))
            return Value(typ, True, yaml_data)
        return Value(typ, False)

    def get_value_type(self, service_ast: Dict[str, Any]) -> None:  # pylint: disable=no-self-use
        """
        Get Value type for ArtifactDefinition object
        :param service_ast: Abstract syntax tree dict
        :return: None
        """
        # TODO: Implement types later.
        return None
