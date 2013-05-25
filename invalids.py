# Remember games we have requested already so we don't waste time requesting them again.

import marks
from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS invalid
(game_id integer primary key)
""")
conn.commit()


def invalidate(game_id):
  cursor.execute( 'INSERT INTO invalid VALUES (?)', [game_id] )
  conn.commit()

def choose_game():
  known_ids = []
  cursor.execute('SELECT max(game_id) FROM invalid')
  known_ids.append( cursor.fetchall()[0][0] )

  cursor.execute('SELECT max(id) FROM games')
  known_ids.append( cursor.fetchall()[0][0] )

  known_ids = [game_id for game_id in known_ids if game_id is not None] + [0]

  return max(known_ids) + 1
