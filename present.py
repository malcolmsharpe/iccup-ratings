from Cheetah.Template import Template
import datetime

import letter
from name_canon import get_name
from starcraft import guess_race, matchups
from tbl import cursor

t = Template(file='templates/leaderboard.html')

class Player(object):
  pass


BASIC_COLUMNS = 8


query = cursor.execute('select * from leaderboard rec order by rec.rank')
records = query.fetchall()
letter_dict = letter.get_dict()
players = []
prev_level = None
run = 0
for rec in records:
  rank, raw_level, nick, mu, sigma, wins, losses, timestamp = rec[:BASIC_COLUMNS]
  mup_counts = rec[BASIC_COLUMNS:]
  player = Player()

  player.level = int( max(raw_level, 0) )
  player.mu = '%.3f' % mu
  player.uncertainty = '%.3f' % (3 * sigma)
  player.rank = rank
  player.games = wins + losses
  player.wins = wins
  player.losses = losses
  player.race = guess_race(mup_counts)
  if timestamp is not None:
    dt = datetime.datetime.fromtimestamp(timestamp)
    # Convert from MSK to PDT.
    dt = dt - datetime.timedelta(hours=11)
    player.last_crawl = dt.strftime('%a %b %d %H:%M PDT')
  else:
    player.last_crawl = 'unknown'

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
