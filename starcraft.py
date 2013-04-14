from collections import Counter, defaultdict

races = 'ptz'
matchups = ['%sv%s' % (r1, r2) for r1 in races for r2 in races]
unordered_matchups = ['tvz', 'zvp', 'pvt']

def make_matchup(a, b):
  return (a + 'v' + b).lower()

def guess_race(mup_counts):
  oppose = defaultdict(lambda: defaultdict(lambda: 0) )
  for mup, count in zip(matchups, mup_counts):
    oppose[ mup[2] ][ mup[0] ] += count

  per_opp = {}
  for r in races:
    games = sum( oppose[r].values() )
    fave = max( races, key=lambda s: oppose[r][s] )
    if oppose[r][fave] > 0.6 * games:
      pick = fave
    else:
      pick = '?'
    per_opp[r] = pick

  choices = Counter( per_opp.values() )
  fave = max( races, key=lambda r: choices[r] )

  if choices[fave] == 3:
    return fave.upper()
  elif choices[fave] == 2:
    excp = max( set('?' + races) - set(fave), key=lambda r: choices[r] )
    assert choices[excp] == 1
    opp, = [r for r in races if per_opp[r] == excp]
    return '%s (%sv%s)' % ( fave.upper(), excp.upper(), opp.upper() )
  elif choices[fave] == 1:
    return ', '.join( ['%sv%s' % ( per_opp[r].upper(), r.upper() ) for r in races] )
  else:
    return '?'
