# May use a game G for rating adjustment if for each player P in the game:
# - mark(P) >= id(G)   (so we've observed all previous games for P)
# - all previous games with P were eligible for rating adjustment
# But only apply the adjustment if secure(P) < id(G)   (so haven't used the game yet).

import marks
from poison import is_poison
from tbl import conn, cursor
import trueskill.trueskill as trueskill


cursor.execute("""
CREATE TABLE IF NOT EXISTS incremental_rating
(nick text primary key, mu real, sigma real, secure int)
""")
conn.commit()


class Player(object):
  def __init__(self, record):
    self.skill = ( record[0], record[1] )
    self.secure = record[2]


def query(nick):
  cursor.execute( 'SELECT mu, sigma, secure FROM incremental_rating WHERE nick = ?', [nick] )
  records = cursor.fetchall()

  if not records:
    records.append( (trueskill.INITIAL_MU, trueskill.INITIAL_SIGMA, 0) )
  record, = records

  return Player(record)


def put(nick_player):
  records = [ [nick, player.skill[0], player.skill[1], player.secure]
    for nick, player in nick_player ]

  cursor.executemany( 'INSERT OR REPLACE INTO incremental_rating VALUES (?, ?, ?, ?)', records)
  conn.commit()


VERBOSE = False


def one_pass():
  LIMIT = 500
  print 'Incremental rating pass with limit %d' % LIMIT

  trueskill.SetParameters(draw_probability=0.0)

  cursor.execute('SELECT id, winner, loser FROM games ORDER BY id')
  records = list( cursor.fetchall() )

  player_mark = marks.get_player_mark()
  incomplete = set()

  num_iter = 0

  for game_id, winner, loser in records:
    if VERBOSE:
      print 'Considering game %d (%s vs %s)' % (game_id, winner, loser)

    players = [winner, loser]
    if any( map(is_poison, players) ) or winner == loser:
      if VERBOSE:
        print '-> game is bad (poisoned player or winner=loser)'
      continue

    eligible = True
    for p in players:
      if player_mark[p] < game_id or p in incomplete:
        if VERBOSE:
          print '-> game is ineligible (%s had old mark or was incomplete)' % p
        eligible = False

    if not eligible:
      for p in players:
        incomplete.add(p)
      continue

    outcome = map(query, players)
    game_applied = [p.secure >= game_id for p in outcome]

    if all(game_applied):
      if VERBOSE:
        print '-> game already applied to ratings'
      continue
    assert not any(game_applied)

    outcome[0].rank = 1
    outcome[1].rank = 2

    trueskill.AdjustPlayers(outcome)

    nick_player = []
    for nick, p in zip(players, outcome):
      p.secure = game_id
      nick_player.append( (nick, p) )
    put(nick_player)

    num_iter += 1
    if num_iter >= LIMIT:
      break

  print 'Applied %d games to ratings' % num_iter
