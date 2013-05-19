# mark table stores when we last queried each player's match list. This is stored as a game ID,
# which is the most recent game we've seen (among all players) after the scrape.

from collections import defaultdict

from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS mark 
(nick text primary key, game_id integer)
""")
conn.commit()


def reset(nick):
  cursor.execute( 'DELETE FROM mark WHERE nick = ?', [nick] )
  conn.commit()


def affirm(nick):
  game_id = cursor.execute('SELECT MAX(id) FROM games').fetchall()[0][0]
  print 'Affirming player %s mark at %d' % (nick, game_id)
  cursor.execute( 'INSERT OR REPLACE INTO mark VALUES (?, ?)', [nick, game_id] )
  conn.commit()


def query(nick):
  cursor.execute( 'SELECT nick, game_id FROM mark WHERE nick = ?', [nick] )
  res = cursor.fetchall()
  if res:
    return res[0][1]
  else:
    return 0


def get_player_mark():
  player_mark = defaultdict(lambda: 0)

  cursor.execute('SELECT nick, game_id FROM mark')
  for nick, game_id in cursor.fetchall():
    player_mark[nick] = game_id

  return player_mark


def choose_player(banned):
  # banned: list of player nicks that aren't eligible (because we had errors on their pages).
  #
  # Try to get rankings that are as accurate as possible by ensuring full player history is known
  # for old games. If every game is understood, then pick a player we think may have played many
  # games we haven't seen.

  player_mark = get_player_mark()

  player_pre = defaultdict(lambda: 0)

  cursor.execute('SELECT id, winner, loser FROM games')
  for game_id, winner, loser in cursor.fetchall():
    for p in [winner, loser]:
      if p not in banned:
        if player_mark[p] < game_id:
          print 'Player %s: mark %d < game ID %d' % (p, player_mark[p], game_id)
          return p
        else:
          player_pre[p] += 1

  max_mark = max( player_mark.values() )
  score_player = []
  players = set( player_pre.keys() )
  for nick in players:
    assert player_mark[nick] > 0
    score = ( max_mark - player_mark[nick] ) * player_pre[nick] / float( player_mark[nick] )
    score_player.append( (score, nick) )

  score, nick = max(score_player)

  print 'Player %s:  pre = %d, mark = %d, max_mark = %d, score = %.1f' % (
    nick, player_pre[nick], player_mark[nick], max_mark, score)

  return nick
