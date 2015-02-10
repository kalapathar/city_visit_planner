import collections


class DaysToPoints(collections.defaultdict):

  def __init__(self, *args, **kwargs):
    super(DaysToPoints, self).__init__(list, *args, **kwargs)

  def Copy(self):
    return DaysToPoints(((i, points[:]) for i, points in self.iteritems()))


def DaysPermutations(points, days_consider):
  results = [DaysToPoints()]
  for point in points:
    next_results = []
    for result in results:
      for i in range(len(days_consider)):
        if not days_consider[i]:
          continue
        next_result = result.Copy()
        next_result[i].append(point)
        next_results.append(next_result)
    results = next_results
  return results