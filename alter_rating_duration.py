# Add three new columns to the games database.

from tbl import conn, cursor
cursor.execute('ALTER TABLE games ADD COLUMN winner_rating text')
cursor.execute('ALTER TABLE games ADD COLUMN loser_rating text')
cursor.execute('ALTER TABLE games ADD COLUMN duration integer')
conn.commit()
