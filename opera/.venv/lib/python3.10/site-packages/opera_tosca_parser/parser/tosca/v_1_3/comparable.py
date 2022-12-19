from __future__ import annotations

from .base import Base


class Comparable(Base):
    def __eq__(self, other: Comparable) -> bool:
        """
        Overridden equals method
        :param other: Other object to compare with
        :return: True if equal else False
        """
        return self.data == other.data

    def __hash__(self):
        """Overridden hash method"""
        return hash(self.data)
