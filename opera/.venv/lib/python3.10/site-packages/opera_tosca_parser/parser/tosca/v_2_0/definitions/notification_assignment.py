from .notification_implementation_definition import NotificationImplementationDefinition
from ..entity import Entity
from ..list import List
from ..map import Map
from ..void import Void


class NotificationAssignment(Entity):
    ATTRS = dict(
        implementation=NotificationImplementationDefinition,
        outputs=Map(List(Void)),
    )
