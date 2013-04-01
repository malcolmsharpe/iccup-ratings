from Cheetah.Template import Template

import letter
from name_canon import get_name
from tbl import cursor

t = Template(file='templates/leaderboard.html')

class Player(object):
  pass

query = cursor.execute('select * from leaderboard rec order by rec.rank')
records = query.fetchall()
letter_dict = letter.get_dict()
players = []
prev_level = None
run = 0
for (rank, raw_level, nick, mu, sigma, wins, losses) in records:
  player = Player()

  player.level = int( max(raw_level, 0) )
  player.mu = '%.3f' % mu
  player.uncertainty = '%.3f' % (3 * sigma)
  player.rank = rank
  player.games = wins + losses
  player.wins = wins
  player.losses = losses

  player.nick = nick
  player.name = get_name(nick)
  if player.name is None:
    player.name = nick

  player.iccup_class, player.iccup_letter = letter_dict.get( nick, ('', '') )

  player.is_header = prev_level != player.level
  if player.is_header:
    run = 0
  player.is_remind = run % 20 == 0

  prev_level = player.level
  run += 1
  players.append(player)


t.players = players

print >>file('html/leaderboard.html', 'w'), t
