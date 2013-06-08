import argparse
from collections import defaultdict
import sys

import marks
from starcraft import make_matchup, matchups
from tbl import conn, cursor
import trueskill.trueskill as trueskill


COLUMNS = 8 + len(matchups)


def persist_leaderboard(limit):
  print 'Clearing leaderboard table'
  sys.stdout.flush()

  cursor.execute("""
  DROP TABLE IF EXISTS leaderboard
  """)

  cursor.execute("""
  CREATE TABLE leaderboard
  (rank integer primary key asc, raw_level real, nick text, mu real, sigma real, wins integer,
  losses integer, timestamp integer, """
  + ', '.join('%s integer' % mup for mup in matchups)
  + """)""")

  cursor.execute("""
  DELETE FROM leaderboard
  """)

  conn.commit()

  class Player(object):
    def __init__(self):
      self.skill = (trueskill.INITIAL_MU, trueskill.INITIAL_SIGMA)
      self.wins = 0
      self.losses = 0

      self.matchups = defaultdict(lambda: 0)

  players = defaultdict( lambda: Player() )

  num_iter = 0
  TALK_INCR = 500

  print 'Fetching marks'
  player_mark = marks.get_player_mark()

  print 'Fetching games'
  sys.stdout.flush()

  query = cursor.execute(
    'SELECT id, winner, loser, winner_race, loser_race, timestamp FROM games2 ORDER BY season, id')
  records = query.fetchall()

  print 'Applying trueskill to %d games' % len(records)
  sys.stdout.flush()

  game_timestamp = {}
  last_game_id = 0
  for (game_id, winner, loser, winner_race, loser_race, timestamp) in records:
    if winner == loser:
      print 'WARNING: game id %d has same winner and loser %s' % (game_id, winner)
      continue

    a = players[winner]
    b = players[loser]

    a.wins += 1
    b.losses += 1

    mup = make_matchup(winner_race, loser_race)
    a.matchups[mup] += 1
    b.matchups[ mup[::-1] ] += 1

    a.rank = 1
    b.rank = 2

    trueskill.AdjustPlayers([a, b])

    num_iter += 1
    if num_iter % TALK_INCR == 0:
      print 'Processed game %6d (id = %6d): %s vs %s' % (num_iter, int(game_id), winner, loser)

    game_timestamp[game_id] = timestamp
    last_game_id = game_id

    if limit is not None and num_iter >= limit:
      break

  player_list = []
  for nick, p in players.items():
    p.nick = nick
    player_list.append(p)
    p.mu, p.sigma = p.skill
    p.level = p.mu - p.sigma * 3.0
    p.timestamp = game_timestamp.get( min( last_game_id, player_mark[nick] ) )
  player_list.sort(key=lambda p: p.level)
  player_list.reverse()

  rows = []
  for i, p in enumerate(player_list):
    rank = i + 1
    row = (rank, p.level, p.nick, p.mu, p.sigma, p.wins, p.losses, p.timestamp)
    row += tuple(p.matchups[mup] for mup in matchups)
    rows.append(row)
  cursor.executemany('INSERT INTO leaderboard VALUES (%s)' % ', '.join('?' * COLUMNS), rows)
  conn.commit()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--limit', type=int,
    help='limit the number of games to process')
  parser.add_argument('--beta', type=float,
    help='beta parameter to trueskill (default %.3f)' % trueskill.BETA)
  parser.add_argument('--gamma', type=float,
    help='gamma parameter to trueskill (default %.3f)' % trueskill.GAMMA)
  args = parser.parse_args()

  trueskill.SetParameters(beta=args.beta, draw_probability=0.0, gamma=args.gamma)

  persist_leaderboard(args.limit)
