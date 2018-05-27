import os
import unittest

import Yusi
from Yusi.YuPoint import city_visit
from Yusi.YuPoint import point
from Yusi.YuPoint import read_csv
from Yusi.YuRanker import age_group_rank_adjuster
from Yusi.YuRanker import rank_adjuster_interface
from Yusi.YuRanker import test_utils


class AgeGroupRankAdjusterTest(test_utils.RankAdjusterTestUtils):
  
  def setUp(self):
    self.points = read_csv.ReadCSVToDict(os.path.join(Yusi.GetYusiDir(), 'YuPoint', 'test_sf_1.csv'))
    self.age_group_rank_adjuster = age_group_rank_adjuster.AgeGroupRankAdjuster()
    super(AgeGroupRankAdjusterTest, self).setUp()
  
  def testGeneral(self):
    score_points_input = [
        rank_adjuster_interface.ScorePoint(100., self.points['Ferry Building']),
        rank_adjuster_interface.ScorePoint(100., self.points['Cable Car']),
        rank_adjuster_interface.ScorePoint(100., self.points['Twin Peaks'])]

    parameters_age_groups = point.AgeGroup(
        senior=None,
        adult=90,
        junior=None,
        child=None,
        toddlers=10)

    city_visit_parameters = city_visit.CityVisitParameters(
        test_utils.MockVisitLocation(),
        day_visit_parameterss=[test_utils.MockDayVisitParameters()],
        point_type=test_utils.MockPointType(),
        age_group=parameters_age_groups)

    score_points_actual = (
        self.age_group_rank_adjuster.AdjustRank(
            score_points_input, city_visit_parameters))

    score_points_expected = [
        rank_adjuster_interface.ScorePoint(16.62, self.points['Ferry Building']),
        rank_adjuster_interface.ScorePoint(13.08, self.points['Cable Car']),
        rank_adjuster_interface.ScorePoint(12.88, self.points['Twin Peaks'])]

    self.assertScorePointsEqual(
        score_points_expected, score_points_actual, places=3)


if __name__ == '__main__':
    unittest.main()
