from enum import Enum


# enum for Lifecycle.Standard operations
class StandardInterfaceOperation(Enum):
    CREATE = "create"
    CONFIGURE = "configure"
    START = "start"
    STOP = "stop"
    DELETE = "delete"

    @classmethod
    def shorthand_name(cls):
        return "Standard"

    @classmethod
    def type_uri(cls):
        return "Lifecycle.Standard"


# enum for Relationship.Configure operations
class ConfigureInterfaceOperation(Enum):
    PRE_CONFIGURE_SOURCE = "pre_configure_source"
    PRE_CONFIGURE_TARGET = "pre_configure_target"
    POST_CONFIGURE_SOURCE = "post_configure_source"
    POST_CONFIGURE_TARGET = "post_configure_target"
    ADD_TARGET = "add_target"
    ADD_SOURCE = "add_source"
    TARGET_CHANGED = "target_changed"
    REMOVE_TARGET = "remove_target"

    @classmethod
    def shorthand_name(cls):
        return "Configure"

    @classmethod
    def type_uri(cls):
        return "Relationship.Configure"


# enum for TOSCA node orchestration states
class NodeState(Enum):
    INITIAL = "initial"
    CREATING = "creating"
    CREATED = "created"
    CONFIGURING = "configuring"
    CONFIGURED = "configured"
    STARTING = "starting"
    STARTED = "started"
    STOPPING = "stopping"
    DELETING = "deleting"
    ERROR = "error"


# enum for TOSCA relationship orchestration states
class RelationshipState(Enum):
    INITIAL = "initial"


# enum for TOSCA operation hosts and reserved TOSCA functions keywords
class OperationHost(Enum):
    SELF = "SELF"
    SOURCE = "SOURCE"
    TARGET = "TARGET"
    ORCHESTRATOR = "ORCHESTRATOR"
