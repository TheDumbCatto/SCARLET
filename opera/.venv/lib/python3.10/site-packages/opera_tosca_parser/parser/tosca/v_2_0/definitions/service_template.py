from __future__ import annotations

import pathlib
import urllib.parse
import urllib.request
from pathlib import PurePath
from typing import Tuple, Set, Dict

from opera_tosca_parser.parser import yaml
from opera_tosca_parser.parser.tosca.v_2_0 import profiles
from opera_tosca_parser.parser.tosca.v_2_0.template.topology import Topology
from opera_tosca_parser.parser.tosca.v_2_0.value import Value
from opera_tosca_parser.parser.yaml.node import Node
from .artifact_type import ArtifactType
from .capability_type import CapabilityType
from .data_type import DataType
from .group_type import GroupType
from .import_definition import ImportDefinition
from .interface_type import InterfaceType
from .node_type import NodeType
from .policy_type import PolicyType
from .relationship_type import RelationshipType
from .repository_definition import RepositoryDefinition
from .topology_template import TopologyTemplate
from .tosca_definitions_version import ToscaDefinitionsVersion
from ..entity import Entity
from ..list import List
from ..map import Map
from ..path import Path
from ..string import String
from ..url import URL


class ServiceTemplate(Entity):
    ATTRS = dict(
        tosca_definitions_version=ToscaDefinitionsVersion,
        # TODO: Add a separate object with validation for profiles if needed.
        profile=String,
        metadata=Map(String),
        description=String,
        # dsl_definitions have already been taken care of by the YAML parser
        repositories=Map(RepositoryDefinition),
        imports=List(ImportDefinition),
        artifact_types=Map(ArtifactType),
        data_types=Map(DataType),
        capability_types=Map(CapabilityType),
        interface_types=Map(InterfaceType),
        relationship_types=Map(RelationshipType),
        node_types=Map(NodeType),
        group_types=Map(GroupType),
        policy_types=Map(PolicyType),
        topology_template=TopologyTemplate,
    )
    REQUIRED = {"tosca_definitions_version"}

    @classmethod
    def normalize(cls, yaml_node: Node) -> Node:
        """
        Normalize ServiceTemplate object
        :param yaml_node: YAML node
        :return: Normalized Node object
        """
        if not isinstance(yaml_node.value, dict):
            cls.abort("TOSCA document should be a map.", yaml_node.loc)

        # Filter out dsl_definitions, since they are preprocessor construct.
        return Node({k: v for k, v in yaml_node.value.items() if k.value != "dsl_definitions"}, yaml_node.loc)

    @classmethod
    def parse_service_template(cls, yaml_node: Node, base_path: pathlib.Path, template_path: pathlib.PurePath,
                               parsed_templates: Set[pathlib.PurePosixPath]) -> Tuple[ServiceTemplate,
                                                                                      Set[pathlib.PurePosixPath]]:
        """
        Parse TOSCA ServiceTemplate object
        :param yaml_node: YAML node
        :param base_path: Base path
        :param template_path: Service template path
        :param parsed_templates: Parsed templates
        :return: Tuple of ServiceTemplate and parsed templates
        """
        service = cls.parse(yaml_node)
        service.visit("prefix_path", template_path.parent)
        parsed = service.merge_imports(yaml_node, base_path, parsed_templates | {template_path})
        return service, parsed

    def merge_imports(self, yaml_node: Node, base_path: pathlib.Path, parsed_templates: Set[pathlib.PurePosixPath]):
        """
        Merge imports for TOSCA service template
        :param yaml_node: YAML node
        :param base_path: Base path
        :param parsed_templates: Parsed templates
        :return: Merged imports
        """
        parsed = parsed_templates.copy()

        for import_def in self.data.get("imports", []):
            file_uri = import_def.get("url", None)
            profile = import_def.get("profile", None)
            repository = import_def.get("repository", None)

            if file_uri and profile:
                self.abort(f"The url and profile keynames are mutually exclusive.", self.loc)

            if not file_uri and not profile:
                self.abort(f"An import statement must include either a url or a profile keyname.", self.loc)

            if profile and repository:
                self.abort("The repository keyname can only be used when a url keyname is specified.", self.loc)

            if file_uri:
                if isinstance(file_uri, URL):
                    file_uri.resolve_url()
                    local_filename, _ = urllib.request.urlretrieve(file_uri.data)
                    import_path = pathlib.PurePath(local_filename)

                    with open(local_filename) as fd:
                        yaml_data = yaml.load(fd, str(import_path))

                    ast, parsed = ServiceTemplate.parse_service_template(yaml_data, base_path, import_path, parsed)
                    self.merge(ast)

                if isinstance(file_uri, Path):
                    file_uri.resolve_path(base_path)
                    import_path = file_uri.data

                    if import_path in parsed:
                        continue

                    with (base_path / import_path).open() as fd:
                        yaml_data = yaml.load(fd, str(import_path))

                    ast, parsed = ServiceTemplate.parse_service_template(yaml_data, base_path, import_path, parsed)
                    self.merge(ast)
                else:
                    self.abort(f"Invalid URI object type: {file_uri}.", self.loc)
            else:
                yaml_data = profiles.load(profile.data, yaml_node)
                ast, parsed = ServiceTemplate.parse_service_template(yaml_data, base_path, PurePath(profile.data),
                                                                     parsed)
                self.merge(ast)

        # We do not need imports anymore, since they are preprocessor construct and would only clutter the AST.
        self.data.pop("imports", None)

        return parsed

    def merge(self, other: ServiceTemplate):
        """
        Merge with other ServiceTemplate object
        :param other: ServiceTemplate object to merge with
        """
        if self.tosca_definitions_version != other.tosca_definitions_version:
            self.abort(
                f"Incompatible TOSCA definitions: {self.tosca_definitions_version} and "
                f"{other.tosca_definitions_version}.", other.loc
            )

        # TODO: Should we merge the topology templates or should we be doing substitution mapping instead?
        for key in (
                "repositories",
                "artifact_types",
                "data_types",
                "capability_types",
                "interface_types",
                "relationship_types",
                "node_types",
                "group_types",
                "policy_types",
                "topology_template"
        ):
            if key not in other.data:
                continue
            if key in self.data:
                self.data[key].merge(other.data[key])
            else:
                self.data[key] = other.data[key]

    def get_template(self, inputs: Dict[str, Value]) -> Topology:
        """
        Get Topology object from template
        :param inputs: Inputs for TOSCA service template
        :return: Topology object
        """
        if "topology_template" not in self:
            return Topology(
                inputs={},
                outputs={},
                nodes={},
                relationships={},
                policies=[]
            )

        return self.topology_template.get_template(inputs, self)
