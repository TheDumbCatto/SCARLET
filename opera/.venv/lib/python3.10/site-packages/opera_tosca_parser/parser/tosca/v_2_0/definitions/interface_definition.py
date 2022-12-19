from .notification_definition import NotificationDefinition
from .operation_definition import OperationDefinition
from .parameter_definition import ParameterDefinition
from ..entity import Entity
from ..map import Map
from ..reference import Reference
from ..string import String


class InterfaceDefinition(Entity):
    ATTRS = dict(
        type=Reference("interface_types"),
        description=String,
        inputs=Map(ParameterDefinition),
        operations=Map(OperationDefinition),
        notifications=Map(NotificationDefinition),
    )
