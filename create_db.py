from tbl import cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS games
(id integer primary key asc, winner text, loser text, winner_race text, loser_race text, map text,
timestamp integer, winner_rating text, loser_rating text, duration integer, winner_precise integer,
loser_precise integer, winner_diff integer)
""")
