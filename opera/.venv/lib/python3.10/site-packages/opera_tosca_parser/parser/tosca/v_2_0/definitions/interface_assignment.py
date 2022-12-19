from .notification_assignment import NotificationAssignment
from .operation_assignment import OperationAssignment
from ..entity import Entity
from ..map import Map
from ..void import Void


class InterfaceAssignment(Entity):
    ATTRS = dict(
        inputs=Map(Void),
        operations=Map(OperationAssignment),
        notifications=Map(NotificationAssignment),
    )
