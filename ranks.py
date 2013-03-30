# nick: URL-friendly name

from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys

from name_canon import register_name
from iccup import urlopen


YEAR = 2013


def ptag_to_nick( ptag, pat=re.compile(r'^gamingprofile/(.*)\.html$') ):
  nick = pat.match( ptag['href'] ).group(1)
  if hasattr(ptag, 'text'):
    register_name(nick, ptag.text)
  return nick
assert ptag_to_nick( {'href': 'gamingprofile/username.html'} ) == 'username'

BIG = 1000000000
def id_to_match_list(player_id, known_max_game_id):
  template = 'http://www.iccup.com/starcraft/matchlist/%s/1x1/page%s.html'

  out = []

  page = 0
  while 1:
    page += 1

    url = template % (player_id, page)
    soup = BeautifulSoup( '\n'.join( urlopen(url) ) )
    print '  ... done parsing.'
    game_tags = soup.find_all('div', 't-corp3')[1:]

    if not game_tags:
      break

    min_game_id = BIG
    for gtag in game_tags:
      player_tags = gtag.find_all( 'a', href=re.compile('gamingprofile') )[2:]

      game_id = int( gtag.find('a', 'game-details')['id'][5:] )

      winner = ptag_to_nick( player_tags[0] )
      loser = ptag_to_nick( player_tags[1] )

      race_tags = gtag.find_all( 'td', text=re.compile('[a-zA-Z]') )
      assert len(race_tags) == 2

      winner_race = race_tags[0].text
      loser_race = race_tags[1].text

      maptag, datetag = gtag.find_all('span', 'textleft')

      map = maptag.text[5:]
      date = datetime.strptime(datetag.text[6:-4] + ' ' + str(YEAR), '%a %b %d %H:%M:%S %Y')
      timestamp = int( time.mktime( date.timetuple() ) )

      out.append( (game_id, winner, loser, winner_race, loser_race, map, timestamp) )
      min_game_id = min(min_game_id, game_id)

    # If no next button, it's definitely the last page of games. Saves one request per player.
    if not soup.find_all('a', text=u'next \xbb'):
      break

    # If we're discovering games from this player that we already knew, abort.
    if min_game_id <= known_max_game_id:
      print 'Breaking early from match list: game id %d less than known max %d' % (
        min_game_id, known_max_game_id)
      break

  return out
