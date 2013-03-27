# nick: URL-friendly name

from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import sys
import urllib2


YEAR = 2013


RETRIES = 30
TIMEOUT = 20
def urlopen(url):
  retry = RETRIES
  while retry > 0:
    retry -= 1
    try:
      print 'Opening %s ...' % url
      sys.stdout.flush()
      lines = list( urllib2.urlopen(url, timeout=TIMEOUT) )
      return lines
    except:
      pass

  print 'ERROR: Failed to get URL'
  return []


nick_to_id_cache = {}

def nick_to_id(nick):
  if nick not in nick_to_id_cache:
    template = 'http://www.iccup.com/starcraft/gamingprofile/%s.html'
    url = template % nick
    pat = re.compile(r'matchlist/([0-9]*)/1x1.html')

    for line in urlopen(url):
      m = pat.search(line)
      if m:
        id = int( m.group(1) )
        break
    else:
      id = None

    nick_to_id_cache[nick] = id

  id = nick_to_id_cache[nick]
  if id is not None:
    return id
  raise ValueError('Invalid nick: ' + nick)


def ptag_to_nick( ptag, pat=re.compile(r'^gamingprofile/(.*)\.html$') ):
  return pat.match( ptag['href'] ).group(1)
assert ptag_to_nick( {'href': 'gamingprofile/username.html'} ) == 'username'

def id_to_match_list(player_id):
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

  return out
