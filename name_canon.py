from tbl import conn, cursor


cursor.execute("""
CREATE TABLE IF NOT EXISTS name_canon
(nick text primary key, name text)
""")

conn.commit()


def register_name(nick, name):
  cursor.execute( 'INSERT OR IGNORE INTO name_canon VALUES (?, ?)', [nick, name] )
  conn.commit()

def get_name(nick):
  query = cursor.execute( 'SELECT * FROM name_canon rec WHERE rec.nick = ?', [nick] )
  results = list( query.fetchall() )

  if not results:
    return None

  return results[0][1]
