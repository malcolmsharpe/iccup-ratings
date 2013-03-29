import sys
import urllib2


class URLError(Exception):
  pass


RETRIES = 30
TIMEOUT = 20
def urlopen(url):
  retry = RETRIES
  while retry > 0:
    retry -= 1
    try:
      print 'Opening %s ...' % url
      sys.stdout.flush()
      lines = list( urllib2.urlopen(url, timeout=TIMEOUT) )
      return lines
    except Exception:
      pass

  print 'ERROR: Failed to get URL'
  raise URLError()
