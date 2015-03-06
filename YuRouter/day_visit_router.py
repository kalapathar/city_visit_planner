from collections import namedtuple
import copy


import Yusi
from Yusi.YuRouter.day_visit_heap import PointsCalculator, DayVisitHeap
from Yusi.YuRouter.day_visit_cost_calculator_interface import DayVisitCostCalculatorGeneratorInterface
from Yusi.YuPoint.point import PointInterface
from Yusi.YuPoint.city_visit import DayVisitParametersInterface


class DayVisitRouterInterface(object):
  """Abstract class which routes points during particular day."""

  def RouteDayVisit(self, all_points, day_visit_parameters):
    """Route maximum number of points with minimum cost for DayVisit."""
    raise NotImplemented()


class DayVisitRouter(DayVisitRouterInterface):
  """Routes points during particular day using permutation and keeping track of
  best so far."""

  def __init__(self, calculator_generator, day_visit_heap_size):
    assert isinstance(calculator_generator,
                      DayVisitCostCalculatorGeneratorInterface)
    assert isinstance(day_visit_heap_size, int)
    
    self.calculator_generator = calculator_generator
    self.day_visit_heap_size = day_visit_heap_size
    
  # TODO(igushev): Use set instead of list for Points.
  def RouteDayVisit(self, all_points, day_visit_parameters):
    for point in all_points:
      assert isinstance(point, PointInterface)
    assert isinstance(day_visit_parameters, DayVisitParametersInterface)

    points_calculator_heap = DayVisitHeap(self.day_visit_heap_size)
    points_calculator_heap.Append(
        PointsCalculator(
            all_points,
            self.calculator_generator.Generate(day_visit_parameters)))
    points_calculator_heap.Shrink()
    while True:
      next_points_calculator_heap = DayVisitHeap(self.day_visit_heap_size)
      pushed_to_next = []
      for points, calculator in (
          points_calculator_heap.GetPointsCalculatorList()):
        for i, point in enumerate(points):
          next_calculator = calculator.Copy()
          pushed_to_next.append(next_calculator.PushPoint(point))
          next_points = points[:i] + points[i+1:]  # -= point
          next_points_calculator_heap.Append(
              PointsCalculator(next_points, next_calculator))
      next_points_calculator_heap.Shrink()
      prev_points_calculator_heap = points_calculator_heap
      points_calculator_heap = next_points_calculator_heap
      if not any(pushed_to_next):
        break
  
    # Return the best.
    assert prev_points_calculator_heap.Size() >= 1
    points_left, calculator_best = (
        prev_points_calculator_heap.GetPointsCalculatorList()[0])
    return (calculator_best.FinalizedDayVisit(),
            calculator_best.GetPointsLeft() + points_left)