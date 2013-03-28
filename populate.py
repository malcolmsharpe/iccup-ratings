import argparse
from collections import deque
import ranks
import sys
from tbl import conn, cursor

mark = set( line.strip() for line in file('completed.txt') )
for player in mark:
  print 'Skipping player %s' % player

queue = deque()

def enqueue(nick):
  if nick in mark:
    return

  print 'Enqueuing player %s' % nick
  mark.add(nick)
  queue.append(nick)


for nick in file('enqueue.txt'):
  enqueue( nick.strip() )


while len(queue):
  current_nick = queue.popleft()

  print 'Processing player %s' % current_nick
  sys.stdout.flush()

  try:
    current_id = ranks.nick_to_id(current_nick)
    print 'ID = %s' % current_id

    matches = ranks.id_to_match_list(current_id)

    for match in matches:
      for player in match[1:3]:
        enqueue(player)

    cursor.executemany('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?)', matches)
    conn.commit()

    print 'Done processing player %s' % current_nick
  except ranks.URLError:
    print 'ERROR: while processing player %s' % current_nick
