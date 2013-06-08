# Drop old data from the previous season.
from tbl import conn, cursor

# The incremental rating table can be recomputed.
cursor.execute('DROP TABLE incremental_rating')

# These tables refer to game IDs from the previous season, so not too useful.
cursor.execute('DROP TABLE invalid')
cursor.execute('DROP TABLE mark')

conn.commit()
