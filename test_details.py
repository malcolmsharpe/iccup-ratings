import unittest

import details

class TestParseFile(unittest.TestCase):
  def test_valid(self):
    ret = details.parse_file('testdata/details_valid.html')
    (game_id, winner, loser, winner_race, loser_race, map, timestamp, winner_letter,
      loser_letter, duration, winner_precise, loser_precise, winner_diff) = ret
    self.assertEqual(game_id, 100000)
    self.assertEqual(winner, 'lonelyday')
    self.assertEqual(loser, 'mospilan')
    self.assertEqual(winner_race, 'P')
    self.assertEqual(loser_race, 'P')
    self.assertEqual(map, '| iCCup | Match Point 1.3')
    self.assertEqual(type(timestamp), int) # FIXME: what should timestamp be?
    self.assertEqual(winner_letter, 'd3')
    self.assertEqual(loser_letter, 'd2')
    self.assertEqual(duration, None) # duration awkward to determine from details page
    self.assertEqual(winner_precise, 2417)
    self.assertEqual(loser_precise, 1456)
    self.assertEqual(winner_diff, 97)

  def test_1v1_race_x(self):
    # These are accepted by the matchlist parser, so they should be accepted here too.

    ret = details.parse_file('testdata/details_1v1_race_x.html')
    (game_id, winner, loser, winner_race, loser_race, map, timestamp, winner_letter,
      loser_letter, duration, winner_precise, loser_precise, winner_diff) = ret
    self.assertEqual(game_id, 376772)
    self.assertEqual(winner, 'sotsoft')
    self.assertEqual(loser, 'onlynoob1')
    self.assertEqual(winner_race, 'x')
    self.assertEqual(loser_race, 'P')
    self.assertEqual(map, '| iCCup | Python 1.3')
    self.assertEqual(type(timestamp), int) # FIXME: what should timestamp be?
    self.assertEqual(winner_letter, 'd2')
    self.assertEqual(loser_letter, 'd1')
    self.assertEqual(duration, None) # duration awkward to determine from details page
    self.assertEqual(winner_precise, 963)
    self.assertEqual(loser_precise, 680)
    self.assertEqual(winner_diff, 75)

  def test_1p_unranked(self):
    ret = details.parse_file('testdata/details_1p_unranked.html')
    self.assertEqual(ret, details.INVALID)

  def test_1v1_unranked(self):
    ret = details.parse_file('testdata/details_1v1_unranked.html')
    self.assertEqual(ret, details.INVALID)

  def test_2v2(self):
    ret = details.parse_file('testdata/details_2v2.html')
    self.assertEqual(ret, details.INVALID)

  def test_3v3_unranked(self):
    ret = details.parse_file('testdata/details_3v3_unranked.html')
    self.assertEqual(ret, details.INVALID)

unittest.main()
