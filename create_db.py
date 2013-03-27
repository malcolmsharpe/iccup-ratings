from tbl import cursor

cursor.execute("""
CREATE TABLE games
(id integer primary key asc, winner text, loser text, winner_race text, loser_race text, map text,
timestamp integer)
""")
