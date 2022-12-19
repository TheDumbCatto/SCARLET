from typing import Any

from opera_tosca_parser.parser.yaml.node import Node
from .loader import Loader


def load(stream: Any, stream_path: str) -> Node:
    """
    Loader function
    :param stream: IO Stream
    :param stream_path: Stream path
    :return: YAML node
    """
    ldr = Loader(stream, stream_path)
    try:
        return ldr.get_single_data()
    finally:
        ldr.dispose()
