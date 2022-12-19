import pkg_resources

from opera_tosca_parser.error import ParseError
from opera_tosca_parser.parser import yaml
from opera_tosca_parser.parser.yaml.node import Node

# TODO: Update according to well-known TOSCA profiles from https://github.com/oasis-open/tosca-community-contributions
# TODO: Tackle these questions after TOSCA 2.0 officially becomes a standard:
#  - How should we store profiles (within the parser, a separate repo, a marketplace)?
#  - How to implement importing versions for well-known profiles?
#  - Will we have to update the parser with every new well known profile version (god please no!)?
#  - Will there be a marketplace for profiles where we could import from?
#  - Could we use our xOpera Template Library to importing profiles from?
#  - Should we create a external function (and CLI command) that will manage TOSCA profiles for parser?


# This is a dict with relative path to profile folder as key and well-known name of TOSCA profile as value
SUPPORTED_TOSCA_PROFILES = dict(
    org_oasis_open_tosca_simple_2_0="org.oasis-open.tosca.simple:2.0"
)


def load(name: str, input_yaml: Node) -> yaml.node.Node:
    """
    Load TOSCA profile
    :param name: Well known TOSCA profile name (e.g., 'org.oasis-open.tosca.simple:2.0')
    :param input_yaml: YAML Node input for TOSCA service template
    :return: YAML node
    """
    if name not in SUPPORTED_TOSCA_PROFILES.values():
        raise ParseError(f"Unsupported TOSCA profile. Available: {', '.join(SUPPORTED_TOSCA_PROFILES.values())}.",
                         input_yaml.loc)

    folder_name = [k for k, v in SUPPORTED_TOSCA_PROFILES.items() if v == name][0]

    # TODO: Rethink if it's okay for profile.yaml to be fixed.
    return yaml.load(pkg_resources.resource_stream(__name__, folder_name + ".yaml"), f"[{name}]")
