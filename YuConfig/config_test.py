import unittest
from Yusi.YuConfig.config import GetDatabaseConnection, GetConfig,\
  GetPointsRanker, GetPointFit, GetCostAccumulatorGenerator,\
  GetDayVisitCostCalculatorGenerator, GetPointsQueueGenerator,\
  GetCityVisitRouter, GetCityVisitFinder, GetCityVisitAccumulatorGenerator,\
  GetCorsOrigin, GetServerParams, GetTaskWorkerParams
from Yusi.YuRouter.day_visit_cost_calculator import DayVisitCostCalculatorGenerator
from Yusi.YuRouter.multi_day_visit_cost_calculator import MultiDayVisitCostCalculatorGenerator


class ConfigTest(unittest.TestCase):

  def setUp(self):
    super(ConfigTest, self).setUp()
    self.config = GetConfig()

  def _SetAndGetDatabaseConnection(self):
    database_connection = GetDatabaseConnection(self.config)
    return database_connection
  
  def testGetDatabaseConnection(self):
    self.assertIsNotNone(self._SetAndGetDatabaseConnection())

  def _SetAndGetPointsRanker(self):
    points_ranker_runner = GetPointsRanker(self.config)
    return points_ranker_runner

  def testGetPointsRanker(self):
    self.assertIsNotNone(self._SetAndGetPointsRanker())

  def _SetAndGetPointFit(self):
    point_fit = GetPointFit(self.config)
    return point_fit 

  def testGetPointFit(self):
    self.assertIsNotNone(self._SetAndGetPointFit())

  def _SetAndGetCostAccumulatorGenerator(self):
    cag_section = 'cost_accumulator_generator'

    self.config.add_section(cag_section)
    for option in ['point_visit_factor',
                   'move_walking_factor',
                   'move_driving_factor',
                   'move_ptt_factor',
                   'lunch_factor',
                   'no_point_visit_factor',
                   'no_point_visit_const',
                   'unused_time_factor']:
      self.config.set(cag_section, option, str(1.))
    cost_accumulator_generator = GetCostAccumulatorGenerator(self.config)
    return cost_accumulator_generator 

  def testGetCostAccumulatorGenerator(self):
    self.assertIsNotNone(self._SetAndGetCostAccumulatorGenerator())

  def _SetAndGetDayVisitCostCalculatorGeneratorDriving(self):
    point_fit = self._SetAndGetPointFit()
    cost_accumulator_generator = self._SetAndGetCostAccumulatorGenerator()
    
    dvccg_section = 'day_visit_const_calculator_generator'
    self.config.add_section(dvccg_section)
    self.config.set(dvccg_section, 'driving_speed', str(20.))
    self.config.set(dvccg_section, 'pause_before_driving', str(0.3))
    self.config.set(dvccg_section, 'walking_speed', str(2.))
    self.config.set(dvccg_section, 'pause_before_walking', str(0.))
    self.config.set(dvccg_section, 'ptt_speed', str(15.))
    self.config.set(dvccg_section, 'pause_before_ptt', str(0.25))
    self.config.set(dvccg_section, 'ptt_cost_mult', str(7.49))
    self.config.set(dvccg_section, 'validate_max_walking_distance', str(True))

    day_visit_const_calculator_generator = (
        GetDayVisitCostCalculatorGenerator(
            self.config,
            point_fit=point_fit,
            cost_accumulator_generator=cost_accumulator_generator))
    return day_visit_const_calculator_generator
    
  def testGetDayVisitCostCalculatorGeneratorDriving(self):
    day_visit_const_calculator_generator = (
        self._SetAndGetDayVisitCostCalculatorGeneratorDriving())
    self.assertIsNotNone(day_visit_const_calculator_generator)
    self.assertTrue(
        isinstance(
            day_visit_const_calculator_generator,
            MultiDayVisitCostCalculatorGenerator))
    self.assertEqual(
        2, len(day_visit_const_calculator_generator.calculator_generators))
    self.assertTrue(
        isinstance(
            day_visit_const_calculator_generator.calculator_generators[0],
            DayVisitCostCalculatorGenerator))
    self.assertTrue(
        isinstance(
            day_visit_const_calculator_generator.calculator_generators[1],
            DayVisitCostCalculatorGenerator))

  def _SetAndGetDayVisitCostCalculatorGeneratorNoDriving(
      self, point_fit, cost_accumulator_generator):
    
    dvccg_section = 'day_visit_const_calculator_generator'
    self.config.add_section(dvccg_section)
    self.config.set(dvccg_section, 'walking_speed', str(2.))
    self.config.set(dvccg_section, 'pause_before_walking', str(0.))
    self.config.set(dvccg_section, 'ptt_speed', str(15.))
    self.config.set(dvccg_section, 'pause_before_ptt', str(0.25))
    self.config.set(dvccg_section, 'ptt_cost_mult', str(7.49))
    self.config.set(dvccg_section, 'validate_max_walking_distance', str(True))

    day_visit_const_calculator_generator = (
        GetDayVisitCostCalculatorGenerator(
            self.config,
            point_fit=point_fit,
            cost_accumulator_generator=cost_accumulator_generator))
    return day_visit_const_calculator_generator

  def testGetDayVisitCostCalculatorGeneratorNoDriving(self):
    point_fit = self._SetAndGetPointFit()
    cost_accumulator_generator = self._SetAndGetCostAccumulatorGenerator()
    day_visit_const_calculator_generator = (
        self._SetAndGetDayVisitCostCalculatorGeneratorNoDriving(
            point_fit, cost_accumulator_generator))
    self.assertIsNotNone(day_visit_const_calculator_generator)
    self.assertTrue(
        isinstance(
            day_visit_const_calculator_generator,
            DayVisitCostCalculatorGenerator))

  def _SetAndGetPointsQueueGenerator(self):
    points_queue_generator = GetPointsQueueGenerator(self.config)
    return points_queue_generator

  def testGetPointsQueueGenerator(self):
    self.assertIsNotNone(self._SetAndGetPointsQueueGenerator())

  def _SetAndGetCityVisitRouter(self):
    point_fit = self._SetAndGetPointFit()
    cost_accumulator_generator = self._SetAndGetCostAccumulatorGenerator()
    self._SetAndGetDayVisitCostCalculatorGeneratorNoDriving(
        point_fit, cost_accumulator_generator)

    cvr_section = 'city_visit_router'
    self.config.add_section(cvr_section)
    for option in ['day_visit_heap_size', 'shard_num_days', 'max_depth',
                   'city_visit_heap_size', 'max_non_pushed_points']:
      self.config.set(cvr_section, option, str(1))
    
    city_visit_router = GetCityVisitRouter(self.config)
    return city_visit_router
  
  def testGetCityVisitRouter(self):
    self.assertIsNotNone(self._SetAndGetCityVisitRouter())

  def _SetAndGetCityVisitFinder(self):
    database_connection = self._SetAndGetDatabaseConnection()
    self._SetAndGetPointsRanker()
    self._SetAndGetCityVisitRouter()
    
    city_visit_finder = GetCityVisitFinder(self.config, database_connection)
    return city_visit_finder

  def testGetCityVisitFinder(self):
    self.assertIsNotNone(self._SetAndGetCityVisitFinder())

  def _SetAndGetCityVisitAccumulatorGenerator(self):
    city_visit_accumulator_generator = (
        GetCityVisitAccumulatorGenerator(self.config))
    return city_visit_accumulator_generator

  def testGetCityVisitAccumulatorGenerator(self):
    self.assertIsNotNone(self._SetAndGetCityVisitAccumulatorGenerator())

  def _SetAndGetCorsOrigin(self):
    cors_section = 'cors'
    self.config.add_section(cors_section)
    self.config.set(cors_section, 'origin', 'test_origin')

    cors_origin = GetCorsOrigin(self.config)
    return cors_origin

  def testGetCorsOrigin(self):
    cors_origin = self._SetAndGetCorsOrigin()
    self.assertEqual('test_origin', cors_origin)

  def _SetAndGetServerParams(self):
    server_section = 'server'
    self.config.add_section(server_section)
    self.config.set(server_section, 'port', '2143')
    self.config.set(server_section, 'host', '0.0.0.0')

    server_port, server_host = GetServerParams(self.config)
    return server_port, server_host

  def testGetServerParams(self):
    server_port, server_host = self._SetAndGetServerParams()
    self.assertEqual(2143, server_port)
    self.assertEqual('0.0.0.0', server_host)

  def _SetAndGetTaskWorkerParams(self):
    tw_section = 'task_worker'
    self.config.add_section(tw_section)
    self.config.set(tw_section, 'idle_seconds_terminate', str(1.5))
    
    idle_seconds_terminate = GetTaskWorkerParams(self.config)
    return idle_seconds_terminate

  def testGetTaskWorkerParams(self):
    idle_seconds_terminate = self._SetAndGetTaskWorkerParams()
    self.assertEqual(1.5, idle_seconds_terminate)



if __name__ == '__main__':
    unittest.main()