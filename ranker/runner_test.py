import unittest

from data import runner_util
from data import test_util as point_test_util
from ranker import runner as ranker_runner
from ranker import test_util as ranker_test_util


class PointsRankerRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    points_input = list(point_test_util.GetPointsInput('data', 'test_sf_1.csv').values())
    points_ranker_runner = ranker_runner.PointsRankerRunner()
    city_visit_parameters = (
        runner_util.GetCityVisitParameters(ranker_test_util.MockVisitLocation(),
                                           [ranker_test_util.MockDayVisitParameters()]))
    points_ranker_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
    unittest.main()
