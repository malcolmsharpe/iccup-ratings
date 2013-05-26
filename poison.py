# Some players are unusable. Maybe something is corrupt in the iCCup database. Hard-code them here
# so that we know we're allowed to skip them when ranking.

POISONED = set(
  [ 'bateriashield7' # player page gives "Wrong Identifier" error
  , 'page0229' # player page gives "Under Construction" error
  , 'twentyeleven' # player page gives "Wrong Identifier" error
  ] )

def is_poison(nick):
  return nick in POISONED
