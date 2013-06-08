import argparse
import re
import sys

from config import CUR_SEASON
import details
import iccup
import incremental
import invalids
import marks
from player import nick_to_id 
import ranks
from tbl import conn, cursor


player_errs = set()
game_errs = set()


def process_player(nick):
  print 'Processing player %s' % nick
  sys.stdout.flush()

  try:
    current_id = nick_to_id(nick)
    print 'ID = %s' % current_id

    matches = ranks.id_to_match_list( current_id, marks.query(nick) )

    cursor.executemany(
      'INSERT OR REPLACE INTO games2 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [ [CUR_SEASON] + list(m) for m in matches] )
    conn.commit()

    marks.affirm(nick)

    print 'Done processing player %s' % nick
  except (iccup.URLError, ValueError), e:
    print 'ERROR: while processing player %s' % nick
    print '  description = %s' % e
    player_errs.add(nick)


def process_game(game_id):
  # Return True when we get something useful.

  print 'Processing game %d' % game_id
  sys.stdout.flush()

  url = 'http://www.iccup.com/starcraft/details/%d.html' % game_id
  html = None
  try:
    lines = iccup.urlopen(url)
    html = '\n'.join(lines)
    ret = details.parse(html)
  except iccup.URLError404:
    # This game might exist in the future.
    pass
  except Exception, e:
    print 'ERROR: While processing game %d' % game_id
    print '  description = %s' % e
    game_errs.add(game_id)
    if html is not None:
      file('last_game_error.html', 'w').write(html)
  else:
    if ret == details.INVALID:
      invalids.invalidate(game_id)
    else:
      cursor.execute(
        'INSERT INTO games2 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        [CUR_SEASON] + list(ret) )
      conn.commit()
      return True

  return False


def main():
  mystery_games = True
  while 1:
    if mystery_games:
      nick = marks.choose_player(player_errs)

      if nick is not None:
        process_player(nick)
      else:
        mystery_games = False
    else:
      game_id = invalids.choose_game()
      if process_game(game_id):
        mystery_games = True

main()
