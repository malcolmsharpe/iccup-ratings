import argparse
import re
import sys

import iccup
import marks
from player import nick_to_id 
import ranks
from tbl import conn, cursor


errs = set()


while 1:
  current_nick = marks.choose_player(errs)

  print 'Processing player %s' % current_nick
  sys.stdout.flush()

  try:
    current_id = nick_to_id(current_nick)
    print 'ID = %s' % current_id

    matches = ranks.id_to_match_list( current_id, marks.query(current_nick) )

    cursor.executemany(
      'INSERT OR REPLACE INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      matches)
    conn.commit()

    marks.affirm(current_nick)

    print 'Done processing player %s' % current_nick
  except (iccup.URLError, ValueError), e:
    print 'ERROR: while processing player %s' % current_nick
    print '  description = %s' % e
    errs.add(current_nick)
