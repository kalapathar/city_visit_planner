import copy

from Yusi.YuPoint.point import PointInterface
from Yusi.YuPoint.city_visit import MoveDescription, MoveType


# TODO(igushev): Do we need to add lunch time to cost?
class CostAccumulatorInterface(object):
  """Abstract class which accumulates cost for a day."""

  def __init__(self):
    self.cost = 0

  def Copy(self):
    return copy.deepcopy(self)

  def Cost(self):
    """Get current cost."""
    return self.cost
  
  def AddPointVisit(self, point):
    """Add visiting point to the cost."""
    raise NotImplemented()

  def AddMoveBetween(self, move_description):
    """Add moving to the cost."""
    raise NotImplemented()

  def AddLunch(self, lunch_hour):
    """Add lunch to the cost."""
    raise NotImplemented()

  def AddPointLeft(self, point):
    """Add point that cannot be visited to the cost."""
    raise NotImplemented()


class CostAccumulatorGeneratorInterface(object):
  """Abstract class which returns every time new clean instance of
  CostAccumulatorInterface."""
  
  def Generate(self):
    """Generate new clean instance of CostAccumulatorInterface."""
    raise NotImplemented()


class FactorCostAccumulator(CostAccumulatorInterface):
  """Accumulates time spent for each action multiplied by a factor."""
  
  def __init__(self,
               point_visit_factor=1.,
               move_walking_factor=1.,
               move_driving_factor=1.,
               move_ptt_factor=1.,
               lunch_factor=1.,
               no_point_visit_factor=1.,
               no_point_visit_const=0.):
    assert isinstance(point_visit_factor, float)
    assert isinstance(move_walking_factor, float)
    assert isinstance(move_driving_factor, float)
    assert isinstance(move_ptt_factor, float)
    assert isinstance(lunch_factor, float)
    assert isinstance(no_point_visit_factor, float)
    assert isinstance(no_point_visit_const, float)

    self._point_visit_factor = point_visit_factor
    self._move_walking_factor = move_walking_factor
    self._move_driving_factor = move_driving_factor
    self._move_ptt_factor = move_ptt_factor
    self._lunch_factor = lunch_factor
    self._no_point_visit_factor = no_point_visit_factor
    self._no_point_visit_const = no_point_visit_const
    super(FactorCostAccumulator, self).__init__()

  def AddPointVisit(self, point):
    assert isinstance(point, PointInterface)

    self.cost += point.duration * self._point_visit_factor

  def AddMoveBetween(self, move_description):
    assert isinstance(move_description, MoveDescription)

    if move_description.move_type == MoveType.walking:
      factor = self._move_walking_factor
    elif move_description.move_type == MoveType.driving:
      factor = self._move_driving_factor
    elif move_description.move_type == MoveType.ptt:
      factor = self._move_ptt_factor
    else:
      raise NotImplemented('Unknown MoveType: %s' % move_description.move_type)
    self.cost += move_description.move_hours * factor

  def AddLunch(self, lunch_hour):
    assert isinstance(lunch_hour, float)

    self.cost += lunch_hour * self._lunch_factor

  def AddPointLeft(self, point):
    assert isinstance(point, PointInterface)

    self.cost += (point.duration * self._no_point_visit_factor +
                  self._no_point_visit_const)


class FactorCostAccumulatorGenerator(CostAccumulatorGeneratorInterface):
  """Returns every time new clean instance of FactorCostAccumulator."""
  
  def __init__(self,
               point_visit_factor=1.,
               move_walking_factor=1.,
               move_driving_factor=1.,
               move_ptt_factor=1.,
               lunch_factor=1.,
               no_point_visit_factor=1.,
               no_point_visit_const=0.):
    assert isinstance(point_visit_factor, float)
    assert isinstance(move_walking_factor, float)
    assert isinstance(move_driving_factor, float)
    assert isinstance(move_ptt_factor, float)
    assert isinstance(lunch_factor, float)
    assert isinstance(no_point_visit_factor, float)
    assert isinstance(no_point_visit_const, float)

    self._point_visit_factor = point_visit_factor
    self._move_walking_factor = move_walking_factor
    self._move_driving_factor = move_driving_factor
    self._move_ptt_factor = move_ptt_factor
    self._lunch_factor = lunch_factor
    self._no_point_visit_factor = no_point_visit_factor
    self._no_point_visit_const = no_point_visit_const

  def Generate(self):
    return FactorCostAccumulator(
        point_visit_factor=self._point_visit_factor,
        move_walking_factor=self._move_walking_factor,
        move_driving_factor=self._move_driving_factor,
        move_ptt_factor=self._move_ptt_factor,
        lunch_factor=self._lunch_factor,
        no_point_visit_factor=self._no_point_visit_factor,
        no_point_visit_const=self._no_point_visit_const)