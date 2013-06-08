# Expand games table's "id" primary key to (season, id) pair.
# The new table is games2.

import os
import os.path

OLD_DB = 'season27.db'
NEW_DB = 'main.db'

if not os.path.exists(NEW_DB):
  os.rename(OLD_DB, NEW_DB)

OLD_SEASON = 24

# Import down here to pick up on the new database filename.
from tbl import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS games2
( season integer, id integer, winner text, loser text, winner_race text, loser_race text, map text,
timestamp integer, winner_rating text, loser_rating text, duration integer, winner_precise integer,
loser_precise integer, winner_diff integer,
PRIMARY KEY (season, id) )
""")
conn.commit()

cursor.execute('SELECT * FROM games')
old_records = cursor.fetchall()

new_records = []
for old_rec in old_records:
  new_rec = [OLD_SEASON] + list(old_rec)
  new_records.append(new_rec)

cursor.executemany('INSERT INTO games2 VALUES (%s)' % ','.join( len( new_records[0] ) * ['?'] ),
  new_records)
conn.commit()

cursor.execute('DROP TABLE games')
conn.commit()
