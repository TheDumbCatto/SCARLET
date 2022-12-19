import pkg_resources

from opera_tosca_parser.parser import yaml


def load(version: str) -> yaml.node.Node:
    """
    Load TOSCA version
    :param version: TOSCA version (e.g., 'v_1_3')
    :return: YAML node
    """
    return yaml.load(pkg_resources.resource_stream(__name__, version + ".yaml"), f"STD[{version}]")
