from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS letter 
(nick text primary key, letter text)
""")
conn.commit()

def note(nick, letter):
  print 'Noting player %s has letter iCCup rank %s' % (nick, letter)
  cursor.execute( 'INSERT OR REPLACE INTO letter VALUES (?, ?)', [nick, letter] )
  conn.commit()
