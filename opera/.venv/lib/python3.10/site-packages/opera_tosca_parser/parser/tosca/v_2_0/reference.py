from __future__ import annotations

from typing import Tuple, Any, Optional, TYPE_CHECKING, Union

from opera_tosca_parser.parser.utils.location import Location
from opera_tosca_parser.parser.yaml.node import Node

if TYPE_CHECKING:
    from opera_tosca_parser.parser.tosca.v_2_0.definitions.service_template import ServiceTemplate

from .string import String
from .type import Type


class ReferenceWrapper(String):
    def __init__(self, data: Any, loc: Optional[Location]):
        """
        Construct ReferenceWrapper object
        :param data: Data
        :param loc: Location object
        """
        super().__init__(data, loc)
        self.section_path: Tuple = ()

    def resolve_reference(self, service_template: ServiceTemplate) -> Any:
        """
        Resolve reference
        :param service_template: ServiceTemplate object
        :return: Resolved target object reference
        """
        if len(self.section_path) == 0:
            raise AssertionError("Missing section path.")

        # Special case for root types that should have no parent
        if self.data == "None":
            return None

        target = service_template.dig(*self.section_path, self.data)
        if not target:
            self.abort(f"Invalid reference {'/'.join(self.section_path + (self.data,))}", self.loc)

        return target


class DataTypeReferenceWrapper(ReferenceWrapper):
    def resolve_reference(self, service_template: ServiceTemplate) -> Any:
        """
        Resolve reference
        :param service_template: ServiceTemplate object
        :return: Resolved target object reference
        """
        if Type.is_valid_internal_type(self.data):
            return Type(self.data, self.loc)
        return super().resolve_reference(service_template)


class MultipleReferenceWrapper(String):
    def __init__(self, data: Any, loc: Optional[Location]):
        """
        Construct MultipleReferenceWrapper object
        :param data: Data
        :param loc: Location object
        """
        super().__init__(data, loc)
        self.section_paths: tuple = ()

    def resolve_reference(self, service_template: ServiceTemplate) -> Any:
        """
        Resolve reference
        :param service_template: ServiceTemplate object
        :return: Resolved target object reference
        """
        if len(self.section_paths) == 0:
            raise AssertionError("Missing section path.")

        # Special case for root types that should have no parent
        if self.data == "None":
            return None

        path_exists = False
        target_result = None
        targets = []
        for section_path in self.section_paths:
            if isinstance(section_path, tuple):
                target = service_template.dig(*section_path, self.data)
            else:
                target = service_template.dig(section_path, self.data)
            if target:
                path_exists = True
                targets.append(target)
                target_result = target

        if len(targets) > 1:
            self.abort(
                f"Duplicate policy targets names were found: "
                f"{str([('/'.join(path_tuple) + '/' + str(self.data)) for path_tuple in self.section_paths])}. Try to "
                f"use unique names.", self.loc
            )

        if not path_exists:
            paths = str([("/".join(path_tuple) if isinstance(path_tuple, tuple) else path_tuple) for path_tuple in
                         self.section_paths])
            self.abort(f"Invalid reference, {str(self.data)} is not in {paths}", self.loc)
        return target_result


class Reference:
    WRAPPER_CLASS = ReferenceWrapper

    def __init__(self, *section_path: Union[str, Tuple[str, ...]]):
        """
        Construct Reference object
        :param section_path: Section path tuple
        """
        if not section_path:
            raise AssertionError("Section path should not be empty.")

        for part in section_path:
            if not isinstance(part, str):
                raise AssertionError("Section path parts should be strings.")

        self.section_path = section_path

    def parse(self, yaml_node: Node) -> ReferenceWrapper:
        """
        Parse YAML Node to Reference object
        :param yaml_node: YAML node
        :return: Parsed object
        """
        ref = self.WRAPPER_CLASS.parse(yaml_node)
        ref.section_path = self.section_path
        return ref


class ReferenceXOR:
    WRAPPER_CLASS = MultipleReferenceWrapper

    def __init__(self, *references: Union[str, Tuple[str, ...]]):
        """
        Construct ReferenceXOR object
        :param references: References tuple
        """
        if not references:
            raise AssertionError("References should not be empty.")
        self.references = references

    def parse(self, yaml_node: Node) -> MultipleReferenceWrapper:
        """
        Parse YAML Node to ReferenceXOR object
        :param yaml_node: YAML node
        :return: Parsed object
        """
        ref = self.WRAPPER_CLASS.parse(yaml_node)
        ref.section_paths = self.references
        return ref


class DataTypeReference(Reference):
    WRAPPER_CLASS = DataTypeReferenceWrapper
