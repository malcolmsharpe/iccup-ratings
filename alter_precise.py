# Add three new columns to the games database.

from tbl import conn, cursor
cursor.execute('ALTER TABLE games ADD COLUMN winner_precise integer')
cursor.execute('ALTER TABLE games ADD COLUMN loser_precise integer')
cursor.execute('ALTER TABLE games ADD COLUMN winner_diff integer')
conn.commit()
