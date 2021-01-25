import uuid

from abc import ABC, abstractmethod
from tuple import Point


class Primitive(ABC):
  def __init__(self):
    self.uid = str(uuid.uuid4)
    self.origin = Point(0, 0, 0)
    super().__init__()

  @abstractmethod
  def intersect(self, ray)
    pass
