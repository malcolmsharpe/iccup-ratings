from collections import defaultdict
import sys
from tbl import conn, cursor
import trueskill.trueskill as trueskill


def persist_leaderboard(limit=None):
  print 'Clearing leaderboard table'
  sys.stdout.flush()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS leaderboard
  (rank integer primary key asc, raw_level real, nick text, mu real, sigma real, games integer)
  """)

  cursor.execute("""
  DELETE FROM leaderboard
  """)

  conn.commit()

  class Player(object):
    def __init__(self):
      self.skill = (trueskill.INITIAL_MU, trueskill.INITIAL_SIGMA)
      self.games = 0

  players = defaultdict( lambda: Player() )

  num_iter = 0
  TALK_INCR = 500

  print 'Fetching games'
  sys.stdout.flush()

  query = cursor.execute('select * from games game order by game.id')
  records = list( query.fetchall() )

  print 'Applying trueskill to %d games' % len(records)
  sys.stdout.flush()

  for (game_id, winner, loser, winner_race, loser_race, map, timestamp) in records:
    a = players[winner]
    b = players[loser]

    a.games += 1
    b.games += 1

    a.rank = 1
    b.rank = 2

    trueskill.AdjustPlayers([a, b])

    num_iter += 1
    if num_iter % TALK_INCR == 0:
      print 'Processed game %6d (id = %6d): %s vs %s' % (num_iter, int(game_id), winner, loser)

    if limit is not None and num_iter >= limit:
      break

  player_list = []
  for name, p in players.items():
    p.name = name
    player_list.append(p)
    p.mu, p.sigma = p.skill
    p.level = p.mu - p.sigma * 3.0
  player_list.sort(key=lambda p: p.level)
  player_list.reverse()

  rows = []
  for i, p in enumerate(player_list):
    rank = i + 1
    rows.append( (rank, p.level, p.name, p.mu, p.sigma, p.games) )
  cursor.executemany('INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?, ?)', rows)
  conn.commit()


if __name__ == '__main__':
  persist_leaderboard()
