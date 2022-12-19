# type: ignore

import collections
from typing import Dict, Any, Tuple, Union

from opera_tosca_parser.parser.tosca.v_2_0.constants import StandardInterfaceOperation, ConfigureInterfaceOperation
from ..entity import TypeEntity


class DefinitionCollectorMixin(TypeEntity):
    def collect_definitions(self, section: str, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA definitions
        :param section: Section of the definitions from TOSCA template
        :param service_ast: Abstract syntax tree dict
        :return: Definitions dict
        """
        defs = {}

        parent = self.derived_from.resolve_reference(service_ast)
        if parent:
            defs.update(parent.collect_definitions(section, service_ast))  # pylint: disable=protected-access
        defs.update(self.get(section, {}))

        return defs

    def collect_types(self, service_ast: Dict[str, Any]) -> Union[Tuple[()], Tuple[str]]:
        """
        Collect TOSCA type definitions
        :param service_ast: Abstract syntax tree dict
        :return: Type definitions tuple or empty tuple
        """
        parent = self.derived_from.resolve_reference(service_ast)
        if not parent:
            return ()
        return (self.derived_from.data,) + parent.collect_types(service_ast)

    def collect_property_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA property definitions
        :param service_ast: Abstract syntax tree dict
        :return: Property definitions dict
        """
        return self.collect_definitions("properties", service_ast)

    def collect_attribute_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA attribute definitions
        :param service_ast: Abstract syntax tree dict
        :return: Attribute definitions dict
        """
        return self.collect_definitions("attributes", service_ast)

    def collect_requirement_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA requirement definitions
        :param service_ast: Abstract syntax tree dict
        :return: Requirement definitions dict
        """
        return self.collect_definitions("requirements", service_ast)

    def collect_capability_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA capability definitions
        :param service_ast: Abstract syntax tree dict
        :return: Capability definitions dict
        """
        return self.collect_definitions("capabilities", service_ast)

    def collect_interface_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA interface definitions
        :param service_ast: Abstract syntax tree dict
        :return: Interface definitions dict
        """
        defs = collections.defaultdict(lambda: dict(inputs={}, operations={}))

        parent = self.derived_from.resolve_reference(service_ast)
        if parent:
            parent_defs = parent.collect_interface_definitions(service_ast)
            for name, definition in parent_defs.items():
                defs[name]["inputs"].update(definition["inputs"])
                defs[name]["operations"].update(definition["operations"])

        for name, definition in self.get("interfaces", {}).items():
            self.check_tosca_standard_and_configure_interfaces(name, definition.get("operations", {}))

            # collect operations and inputs from linked interface_types
            if definition.get("type", None):
                parent_interface_type = definition.type.resolve_reference(service_ast)
                if parent_interface_type:
                    defs[name]["inputs"].update(parent_interface_type.get("inputs", {}))
                    defs[name]["operations"].update(parent_interface_type.get("operations", {}))

            defs[name]["inputs"].update(definition.get("inputs", {}))
            defs[name]["operations"].update(definition.get("operations", {}))

        return dict(defs)

    def check_tosca_standard_and_configure_interfaces(self, interface_name: str, operations: Dict[str, Any]):
        """
        Check TOSCA Standard and Configure interfaces
        :param interface_name: TOSCA interface name
        :param operations: TOSCA interface operations
        """
        standard_interface_names = [StandardInterfaceOperation.shorthand_name(),
                                    StandardInterfaceOperation.type_uri()]
        configure_interface_names = [ConfigureInterfaceOperation.shorthand_name(),
                                     ConfigureInterfaceOperation.type_uri()]

        if interface_name in standard_interface_names:
            valid_standard_interface_operation_names = [i.value for i in StandardInterfaceOperation]
            for operation in operations:
                if operation not in valid_standard_interface_operation_names:
                    self.abort(
                        f"Invalid operation for {interface_name} interface: {operation}. Valid operation names are: "
                        f"{valid_standard_interface_operation_names}.", self.loc
                    )

        if interface_name in configure_interface_names:
            valid_configure_interface_operation_names = [i.value for i in ConfigureInterfaceOperation]
            for operation in operations:
                if operation not in valid_configure_interface_operation_names:
                    self.abort(
                        f"Invalid operation for {interface_name} interface: {operation}. Valid operation names are: "
                        f"{valid_configure_interface_operation_names}.", self.loc
                    )

    def collect_artifact_definitions(self, service_ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect TOSCA artifact definitions
        :param service_ast: Abstract syntax tree dict
        :return: Artifact definitions dict
        """
        return self.collect_definitions("artifacts", service_ast)
