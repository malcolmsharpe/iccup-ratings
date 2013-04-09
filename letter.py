from tbl import conn, cursor

# This table DEPRECATED. Player rankings are now stored in the games table.
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
  'a1': 'A&#x2212;',
  'b3': 'B+',
  'b2': 'B',
  'b1': 'B&#x2212;',
  'c3': 'C+',
  'c2': 'C',
  'c1': 'C&#x2212;',
  'd3': 'D+',
  'd2': 'D',
  'd1': 'D&#x2212;',
  'cpu': 'CPU',
}


def precise_to_letter(x):
  # http://www.iccup.com/starcraft/sc_rating_system.html
  # List not updated for CPU rank. My guess is 0 - 399.

  if x < 400: return 'cpu'
  if x < 850: return 'd1'
  if x < 2000: return 'd2'
  if x < 3000: return 'd3'
  if x < 4000: return 'c1'
  if x < 5000: return 'c2'
  if x < 6000: return 'c3'
  if x < 7000: return 'b1'
  if x < 8000: return 'b2'
  if x < 9000: return 'b3'
  if x < 10500: return 'a1'
  if x < 12000: return 'a2'
  if x < 15000: return 'a3'

  raise ValueError('Olympic rank not supported')


def get_dict():
  raw = {}

  # First use the old letter database.
  for nick, letter in cursor.execute('SELECT * FROM letter').fetchall():
    raw[nick] = letter

  # Then use the games table, as recently as possible.
  for (winner, loser, winner_rating, loser_rating, winner_precise, loser_precise,
    winner_diff) in cursor.execute('SELECT winner, loser, winner_rating, loser_rating, '
      'winner_precise, loser_precise, winner_diff FROM games game ORDER BY game.id'):
    if winner_rating is not None:
      raw[winner] = winner_rating
    if loser_rating is not None:
      raw[loser] = loser_rating
    if winner_precise is not None and winner_diff is not None:
      precise = winner_precise + winner_diff
      raw[winner] = precise_to_letter(precise)

  # Format for HTML.
  out = {}

  for nick, letter in raw.items():
    iccup_class = letter_to_class[letter]
    iccup_letter = letter_to_pretty[letter]
    out[nick] = (iccup_class, iccup_letter)

  return out
