import argparse
from collections import deque
import re
import sys

from player import nick_to_id 
import ranks
from tbl import conn, cursor
import iccup


mark = set()
queue = deque()

def enqueue(nick):
  if nick in mark:
    return

  print 'Enqueuing player %s' % nick
  mark.add(nick)
  queue.append(nick)


def restart(log_path):
  print 'Restarting from previous log %s' % log_path
  skip_pat = re.compile(r'(?:Skipping player|Done processing player) (.*)$')
  enq_pat = re.compile(r'Enqueuing player (.*)$')
  to_enqueue = []
  for line in file(log_path):
    m = skip_pat.match(line)
    if m:
      print 'Skipping player %s' % m.group(1).strip()
      mark.add( m.group(1) )
    m = enq_pat.match(line)
    if m:
      to_enqueue.append( m.group(1).strip() )
  for nick in to_enqueue:
    enqueue(nick)
  print 'Done restart'

if len(sys.argv) > 1:
  restart( sys.argv[1] )


while len(queue):
  current_nick = queue.popleft()

  print 'Processing player %s' % current_nick
  sys.stdout.flush()

  try:
    current_id = nick_to_id(current_nick)
    print 'ID = %s' % current_id

    matches = ranks.id_to_match_list(current_id)

    for match in matches:
      for player in match[1:3]:
        enqueue(player)

    cursor.executemany('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?)', matches)
    conn.commit()

    print 'Done processing player %s' % current_nick
  except (iccup.URLError, ValueError):
    print 'ERROR: while processing player %s' % current_nick
