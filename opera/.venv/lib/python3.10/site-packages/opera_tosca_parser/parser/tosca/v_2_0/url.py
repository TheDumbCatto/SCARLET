from __future__ import annotations

from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from opera_tosca_parser.parser.yaml.node import Node
from .string import String


class URL(String):
    @classmethod
    def build(cls, yaml_node: Node) -> URL:
        """
        Build Path object from YAML node
        :param yaml_node: YAML node
        :return: Path object
        """
        return cls(yaml_node.value, yaml_node.loc)

    def resolve_url(self):
        """Resolve path"""
        self.data = self.data.strip()
        self._validate_url()

    def _validate_url(self):
        """Validate URL"""
        url = self.data

        parsed_url = urlparse(url)
        supported_url_schemes = ("https", "http", "file")
        if parsed_url.scheme not in supported_url_schemes:
            self.abort(
                f"URL {url} has invalid URL scheme, supported are: {', '.join(supported_url_schemes)}.", self.loc
            )

        if len(url) > 2048:
            self.abort(f"URL {url} exceeds maximum length of 2048 characters.", self.loc)

        if not parsed_url.netloc:
            self.abort(f"No URL domain specified in {url}.", self.loc)

        try:
            urlopen(url)
        except URLError as e:
            self.abort(f"Cannot open URL {url}, error: {e}.", self.loc)
