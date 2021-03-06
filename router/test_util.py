import os

from data import point as point_
from data import city_visit
from data import read_csv
from router import move_calculator


class MockCoordinates(point_.CoordinatesInterface):
  def __init__(self, name):
    assert isinstance(name, str)
    self.name = name

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __str__(self):
    return self.name


def MockPoints():
  points = read_csv.ReadCSVToDict(os.path.join('data', 'test_sf_1.csv'))
  for point in list(points.values()):
    point.coordinates_starts = MockCoordinates(point.name)
    point.coordinates_ends = MockCoordinates(point.name)
  return points


# NOTE(igushev): Here we mock Coordinates with simple str and in this
# dictionary just define move_description between two given points.
# MockMoveCalculator relies instead of some sort of calculation of this
# dictionary.
MOVE_HOURS = {frozenset({'Hotel', 'Ferry Building'}): 1.,
              frozenset({'Hotel', 'Pier 39'}): 3.,
              frozenset({'Hotel', 'Golden Gate Bridge'}): 6.,
              frozenset({'Hotel', 'Union Square'}): 1.,
              frozenset({'Hotel', 'Twin Peaks'}): 3.,
              frozenset({'Hotel', 'Restaurant'}): 1.,
              frozenset({'Ferry Building', 'Pier 39'}): 1.,
              frozenset({'Ferry Building', 'Golden Gate Bridge'}): 8.,
              frozenset({'Ferry Building', 'Union Square'}): 2.,
              frozenset({'Ferry Building', 'Twin Peaks'}): 5.,
              frozenset({'Ferry Building', 'Restaurant'}): 2.,
              frozenset({'Pier 39', 'Golden Gate Bridge'}): 5.,
              frozenset({'Pier 39', 'Union Square'}): 2.,
              frozenset({'Pier 39', 'Twin Peaks'}): 5.,
              frozenset({'Pier 39', 'Restaurant'}): 4.,
              frozenset({'Golden Gate Bridge', 'Union Square'}): 5.,
              frozenset({'Golden Gate Bridge', 'Twin Peaks'}): 5.,
              frozenset({'Golden Gate Bridge', 'Restaurant'}): 6.,
              frozenset({'Twin Peaks', 'Union Square'}): 3.,
              frozenset({'Twin Peaks', 'Restaurant'}): 2.,
              frozenset({'Union Square', 'Restaurant'}): 1.}


class MockMoveCalculator(move_calculator.MoveCalculatorInterface):
  def CalculateMoveDescription(self, coordinates_from, coordinates_to):
    coordinates_between = (
      frozenset({coordinates_from.name, coordinates_to.name}))
    if not coordinates_between in MOVE_HOURS:
      raise AssertionError(
          'MOVE_HOURS is not defined between coordinates: %s and %s' % (
              coordinates_from, coordinates_to))
    return city_visit.MoveDescription(coordinates_from, coordinates_to,
                                      MOVE_HOURS[coordinates_between], city_visit.MoveType.walking)
