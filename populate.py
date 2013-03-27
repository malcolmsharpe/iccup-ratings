import argparse
from collections import deque
import ranks
import sys
from tbl import conn, cursor

mark = set()
queue = deque()

def enqueue(nick):
  if nick in mark:
    return

  print 'Enqueuing player %s' % nick
  mark.add(nick)
  queue.append(nick)


start_nick = sys.argv[1]
enqueue(start_nick)


while len(queue):
  current_nick = queue.popleft()
  print 'Processing player %s' % current_nick
  sys.stdout.flush()

  current_id = ranks.nick_to_id(current_nick)
  print 'ID = %s' % current_id

  matches = ranks.id_to_match_list(current_id)

  for match in matches:
    for player in match[1:3]:
      enqueue(player)

  cursor.executemany('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?)', matches)
  conn.commit()

  print 'Done processing player %s' % current_nick
