import unittest

from router import runner as router_runner
from data import test_util


class CityVisitRouterRunnerTest(unittest.TestCase):
  
  def testGeneral(self):
    points_dict = test_util.GetPointsInput('data', 'test_sf_1.csv')
    points_keys = test_util.GetPointsKeys('router', 'test_points_sf.txt')
    points_input = test_util.FilterAndSortByKeys(points_dict, points_keys)
  
    start_end_coordinates = points_dict['Union Square'].coordinates_starts
    first_day, last_day = 1, 2
    day_visit_parameterss = router_runner.GetDayVisitParameterss(start_end_coordinates, first_day, last_day)
    
    city_visit_router_runner = router_runner.CityVisitRouterRunner()
    city_visit_router_runner.Run(points_input, day_visit_parameterss)


if __name__ == '__main__':
    unittest.main()