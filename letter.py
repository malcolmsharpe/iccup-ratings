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


letter_to_class = {
  'a3': 'ranka',
  'a2': 'ranka',
  'a1': 'ranka',
  'b3': 'rankb',
  'b2': 'rankb',
  'b1': 'rankb',
  'c3': 'rankc',
  'c2': 'rankc',
  'c1': 'rankc',
  'd3': 'rankd',
  'd2': 'rankd',
  'd1': 'rankd',
  'cpu': 'rankd',
}

letter_to_pretty = {
  'a3': 'A+',
  'a2': 'A',
  'a1': 'A-',
  'b3': 'B+',
  'b2': 'B',
  'b1': 'B-',
  'c3': 'C+',
  'c2': 'C',
  'c1': 'C-',
  'd3': 'D+',
  'd2': 'D',
  'd1': 'D-',
  'cpu': 'CPU',
}


def get_dict():
  out = {}
  for nick, letter in cursor.execute('SELECT * FROM letter').fetchall():
    iccup_class = letter_to_class[letter]
    iccup_letter = letter_to_pretty[letter]
    out[nick] = (iccup_class, iccup_letter)
  return out
