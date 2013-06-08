from Cheetah.Template import Template
from collections import defaultdict

from starcraft import make_matchup, matchups, unordered_matchups
from tbl import cursor
from timeutil import format_timestamp

t = Template(file='templates/maps.html')

cursor.execute('SELECT winner_race, loser_race, map, timestamp FROM games2')

stats = defaultdict( lambda: defaultdict(lambda: 0) )

max_timestamp = None
for winner_race, loser_race, map, timestamp in cursor.fetchall():
  mup = make_matchup(winner_race, loser_race)
  if mup in matchups:
    stats[map][mup] += 1
  if max_timestamp is None or timestamp > max_timestamp:
    max_timestamp = timestamp

class Map(object):
  pass

class Mup(object):
  pass

t.last_crawl = format_timestamp(max_timestamp)
t.maps = []

for map in stats:
  m = Map()
  m.name = map
  m.games = sum( stats[map].values() )
  m.mups = []
  for mup in unordered_matchups:
    pum = mup[::-1]
    obj = Mup()
    obj.r1 = mup[0].upper()
    obj.r2 = mup[2].upper()
    obj.wins = stats[map][mup]
    obj.losses = stats[map][pum]
    if obj.wins + obj.losses > 0:
      obj.pct = '%.f%%' % ( 100.0 * obj.wins / (obj.wins + obj.losses) )
    else:
      obj.pct = 'N/A'
    m.mups.append(obj)
  t.maps.append(m)

t.maps.sort(key=lambda m: m.games, reverse=True)

print >>file('html/maps.html', 'w'), t
