import re

from iccup import urlopen
from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS nick_id
(nick text primary key asc, id integer)
""")

conn.commit()


def nick_to_id(nick):
  query = cursor.execute('SELECT * FROM nick_id rec WHERE rec.nick = ?', [nick])
  recs = query.fetchall()

  if recs:
    nick, id = recs[0]
    return id


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

  if id is not None:
    cursor.execute( 'INSERT OR IGNORE INTO nick_id VALUES (?, ?)', [nick, id] )
    conn.commit()

    return id
  raise ValueError('Invalid nick: ' + nick)
