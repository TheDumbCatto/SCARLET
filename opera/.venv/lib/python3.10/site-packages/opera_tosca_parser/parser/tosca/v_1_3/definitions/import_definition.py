from opera_tosca_parser.parser.tosca.v_1_3.entity import Entity
from opera_tosca_parser.parser.tosca.v_1_3.path import Path
from opera_tosca_parser.parser.tosca.v_1_3.string import String
from opera_tosca_parser.parser.yaml.node import Node


class ImportDefinition(Entity):
    ATTRS = dict(
        file=Path,
        repository=String,
        namespace_prefix=String,
        namespace_uri=String,
    )
    DEPRECATED = {
        "namespace_uri",
    }

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize ImportDefinition object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, (str, dict)):
            cls.abort("Invalid import data. Expected string or dict.", yaml_node.loc)
        if isinstance(yaml_node.value, str):
            return Node({Node("file"): yaml_node})
        return yaml_node
