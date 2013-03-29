from Cheetah.Template import Template
from name_canon import get_name
from tbl import cursor

t = Template(file='templates/leaderboard.html')

TEXT_OUTPUT = False

class Player(object):
  pass

query = cursor.execute('select * from leaderboard rec order by rec.rank')
records = list( query.fetchall() )
players = []
prev_level = None
run = 0
for (rank, raw_level, nick, mu, sigma, games) in records:
  player = Player()

  player.level = int( max(raw_level, 0) )
  player.mu = '%.3f' % mu
  player.uncertainty = '%.3f' % (3 * sigma)
  player.rank = rank
  player.games = games

  player.nick = nick
  player.name = get_name(nick)
  if player.name is None:
    player.name = nick

  player.is_header = prev_level != player.level
  if player.is_header:
    run = 0
  player.is_remind = run % 20 == 0

  prev_level = player.level
  run += 1
  players.append(player)


if TEXT_OUTPUT:
  f = file('html/leaderboard.txt', 'w')
  print >>f, '=== Leaderboard ==='
  for player in players:
    print >>f, '%02d  %6s +/- %6s  %4d  %3d   %s' % (player.level, player.mu, player.uncertainty,
      player.rank, player.games, player.nick)


t.players = players

print >>file('html/leaderboard.html', 'w'), t
