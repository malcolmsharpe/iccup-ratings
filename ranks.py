# nick: URL-friendly name

from bs4 import BeautifulSoup
import re
import urllib2


def urlopen(url):
  print 'Opening %s' % url
  return urllib2.urlopen(url)


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

def id_to_match_list(id):
  template = 'http://www.iccup.com/starcraft/matchlist/%s/1x1/page%s.html'

  out = []

  page = 0
  while 1:
    page += 1

    url = template % (id, page)
    soup = BeautifulSoup( urlopen(url) )
    game_tags = soup.find_all('div', 't-corp3')[1:]

    if not game_tags:
      break

    for gtag in game_tags:
      player_tags = gtag.find_all( 'a', href=re.compile('gamingprofile') )[2:]
      players = map(ptag_to_nick, player_tags)
      out.append(players)

  return out
