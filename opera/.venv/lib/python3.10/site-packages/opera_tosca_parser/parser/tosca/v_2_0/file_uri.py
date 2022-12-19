from __future__ import annotations

import pathlib
from typing import Union
from urllib.parse import urlparse

from opera_tosca_parser.parser.yaml.node import Node
from .path import Path
from .string import String
from .url import URL


class FileURI(String):
    @classmethod
    def build(cls, yaml_node: Node) -> Union[Path, URL]:
        """
        Build FileURI object from YAML node
        :param yaml_node: YAML node
        :return: Path or URL object
        """
        if not yaml_node:
            cls.abort("No URL or path has been specified. ", yaml_node.loc)

        parsed_uri = urlparse(yaml_node.value)
        if parsed_uri.scheme:
            return URL(yaml_node.value, yaml_node.loc)
        else:
            return Path(pathlib.PurePath(yaml_node.value), yaml_node.loc)
