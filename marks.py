# mark table stores when we last queried each player's match list. This is stored as a game ID,
# which is the most recent game we've seen (among all players) after the scrape.

from collections import defaultdict

from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS mark 
(nick text primary key, game_id integer)
""")
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
    return res[1]
  else:
    return 0


def choose_player():
  player_mark = defaultdict(lambda: 0)

  cursor.execute('SELECT nick, game_id FROM mark')
  for nick, game_id in cursor.fetchall():
    player_mark[nick] = game_id

  player_pre = defaultdict(lambda: 0)
  player_post = defaultdict(lambda: 0)

  cursor.execute('SELECT id, winner, loser FROM games')
  for game_id, winner, loser in cursor.fetchall():
    for p in [winner, loser]:
      if game_id > player_mark[p]:
        player_post[p] += 1
      else:
        player_pre[p] += 1

  max_mark = max( player_mark.values() )
  score_player = []
  players = set( player_mark.keys() + player_pre.keys() + player_post.keys() )
  for nick in players:
    score = player_post[nick]
    if player_mark[nick] > 0:
      score += ( max_mark - player_mark[nick] ) * player_pre[nick] / player_mark[nick]
    score_player.append( (score, nick) )

  score, nick = max(score_player)

  print 'Player %s:  pre = %d, post = %d, mark = %d, max_mark = %d' % (
    nick, player_pre[nick], player_post[nick], player_mark[nick], max_mark)

  return nick
