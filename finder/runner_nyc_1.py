from data import city_visit
from data import point
from data import runner_util
from data import test_util as point_test_util
from finder import runner as finder_runner


def main():
  points_input = list(point_test_util.GetPointsInput('data', 'test_nyc_1.csv').values())
  city_visit_finder_runner = finder_runner.CityVisitFinderRunner()
  visit_location = city_visit.VisitLocation('New York City')
  # 746 Ninth Ave, New York, NY 10019.
  start_end_coordinates = point.Coordinates(40.763582, -73.988470)
  first_day, last_day = 13, 16
  day_visit_parameterss = runner_util.GetDayVisitParameterss(start_end_coordinates, first_day, last_day)
  city_visit_parameters = runner_util.GetCityVisitParameters(visit_location, day_visit_parameterss)
  
  city_visit_finder_runner.Run(points_input, city_visit_parameters)


if __name__ == '__main__':
  main()
