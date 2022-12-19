from typing import Any, Optional

from opera_tosca_parser.parser.utils.location import Location


class Node:
    def __init__(self, value: Any, loc: Optional[Location] = None):
        """
        Construct YAML Node object
        :param value: Node value
        :param loc: Node location
        """
        self.value = value
        self.loc = loc or Location("", 0, 0)

    @property
    def bare(self) -> Any:
        """
        Return bare YAML node value
        :return: YAML node value
        """
        if isinstance(self.value, list):
            return [v.bare for v in self.value]
        if isinstance(self.value, dict):
            return {k.bare: v.bare for k, v in self.value.items()}
        return self.value

    def __str__(self) -> str:
        """Overridden string representation"""
        return f"Node({self.loc})[{self.bare}]"
