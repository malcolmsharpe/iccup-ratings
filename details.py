from bs4 import BeautifulSoup
import re

import timeutil

INVALID = 'INVALID'

def parse_file(f):
  return parse( '\n'.join( file(f) ) )

# iCCup &mdash; Game Details / 100000
title_pat = re.compile(r'Game Details / ([0-9]+)')

# profile/view/LonelyDay.html
# gamingprofile/smokeybear.html
profile_pat = re.compile(r'^(?:profile/view|gamingprofile)/(.*).html$')

def parse(s):
  soup = BeautifulSoup(s)

  title_tag = soup.find('title')
  game_id = int( title_pat.search(title_tag.text).group(1) )

  player_tags = soup.find_all('div', 'field1 width170')
  if len(player_tags) != 2:
    return INVALID

  players = []
  for ptag in player_tags:
    atag = ptag.find('a', href=profile_pat)
    name = profile_pat.search( atag['href'] ).group(1)
    nick = name.lower()

    race_tag = ptag.parent.find('div', 'field2')
    race = race_tag.text[0]

    diff_tag = race_tag.find('b')
    try:
      diff = int(diff_tag.text)
    except ValueError:
      return INVALID

    letter_tag = ptag.find('div')
    letter, = letter_tag['class']
    precise = int( letter_tag['title'] )

    players.append( (diff, nick, race, letter, precise) )
  players.sort()

  loser_diff, loser, loser_race, loser_letter, loser_precise = players[0]
  winner_diff, winner, winner_race, winner_letter, winner_precise = players[1]

  start_tag = soup.find('div', text='Start Game')
  date_tag = start_tag.parent.find('div', 'field2')
  # Sat Mar 23 18:58:01 MSK
  timestamp = timeutil.parse_date(date_tag.text)

  map_tag = soup.find('div', 'field1 width160', text='Map')
  map = map_tag.parent.find('a').text

  return (game_id
         ,winner
         ,loser
         ,winner_race
         ,loser_race
         ,map
         ,timestamp
         ,winner_letter
         ,loser_letter
         ,None
         ,winner_precise
         ,loser_precise
         ,winner_diff
         )
