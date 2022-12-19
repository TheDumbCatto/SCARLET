from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from opera_tosca_parser.parser.tosca.v_1_3.constants import OperationHost

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_1_3.value import Value


class Operation:
    def __init__(self, name: str, primary: str, dependencies: List[str], artifacts: List[str], inputs: Dict[str, Value],
                 outputs: Dict[str, Value], timeout: str, host: OperationHost):
        """
        Construct a new Operation object
        :param name: Operation name
        :param primary: Operation primary artifact
        :param dependencies: Operation dependencies
        :param artifacts: Operation artifacts
        :param inputs: Operation inputs
        :param outputs: Operation outputs
        :param timeout: Operation timeout
        :param host: Operation host
        """
        self.name = name
        self.primary = primary
        self.dependencies = dependencies
        self.artifacts = artifacts
        self.inputs = inputs
        self.outputs = outputs
        self.timeout = timeout
        self.host = host
