import json
import sys

from tbl import conn, cursor

path = 'html/games.json'

query = cursor.execute('select * from games game order by game.id')
records = query.fetchall()

print 'Dumping %d games to JSON at %s' % (len(records), path)
sys.stdout.flush()

core = []
for game in records:
  core.append( json.dumps(game) )

target = '[' + ', '.join(core) + ']'
validation = json.dumps(records)

if target != validation:
  print 'WARNING: target != validation'
  file('target.dump', 'w').write(target)
  file('validation.dump', 'w').write(validation)

f = file(path, 'w')
print >>f, '[\n' + ',\n'.join(core) + '\n]'
