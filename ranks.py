# nick: URL-friendly name

from bs4 import BeautifulSoup
import re
import sys

from iccup import urlopen
import letter
from name_canon import register_name
import timeutil


def ptag_to_nick( ptag, pat=re.compile(r'^gamingprofile/(.*)\.html$') ):
  nick = pat.match( ptag['href'] ).group(1)
  if hasattr(ptag, 'text'):
    register_name(nick, ptag.text)
  return nick
assert ptag_to_nick( {'href': 'gamingprofile/username.html'} ) == 'username'

BIG = 1000000000
dur_pat = re.compile(r'([0-9]+) : ([0-9]+)')
diff_pat = re.compile(r'^[+-][0-9]+$')
def id_to_match_list(player_id, known_max_game_id):
  template = 'http://www.iccup.com/starcraft/matchlist/%s/1x1/page%s.html'

  out = []

  noted_letter = False
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
      # Date: Sat Mar 23 18:58:01 MSK
      timestamp = timeutil.parse_date( datetag.text[6:] )

      rank_divs = gtag.find_all( 'div', title=re.compile(r'[0-9]+') )
      if len(rank_divs) == 2:
        letters = []
        precises = []

        for rdiv, ptag in zip(rank_divs, player_tags):
          lett = rdiv['class'][0]
          try:
            prec = int( rdiv['title'] )
          except ValueError:
            prec = None
          letters.append(lett)
          precises.append(prec)
          if not noted_letter and 'bold' in ptag.get( 'style', [] ):
            letter.note(ptag_to_nick(ptag), lett)
            noted_letter = True
        assert len(letters) == 2
        assert len(precises) == 2

        winner_letter, loser_letter = letters
        winner_precise, loser_precise = precises
      else:
        print 'WARNING: game %d has strange number of rank divs' % game_id

      duration = None
      dtag = gtag.find('div', 'field8 width60')
      if dtag is None:
        print 'WARNING: game %d has no duration' % game_id
      else:
        bold_tag = dtag.find('b')

        if bold_tag is None:
          dur_str = dtag.text
        else:
          dur_str = bold_tag.text

        m = dur_pat.match(dur_str)
        if m is None:
          print 'WARNING: game %d has weird duration' % game_id
        else:
          duration = 60 * int( m.group(1) ) + int( m.group(2) )

      winner_diff = None
      ftag = gtag.find('b', text=diff_pat)
      if ftag is None:
        print 'WARNING: game %d has no winner diff' % game_id
      else:
        winner_diff = int(ftag.text)

      out.append( (game_id, winner, loser, winner_race, loser_race, map, timestamp, winner_letter,
        loser_letter, duration, winner_precise, loser_precise, winner_diff) )
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
