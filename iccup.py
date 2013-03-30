import sys
import time
import urllib2


class URLError(Exception):
  pass


# http://iccup.com/robots.txt
# User-agent: *
# Crawl-delay: 15
CRAWL_DELAY = 15
last_crawl = None

RETRIES = 30
TIMEOUT = 20
def urlopen(url):
  global last_crawl
  retry = RETRIES
  while retry > 0:
    retry -= 1
    try:
      now = time.time()
      if last_crawl is not None:
        stall = last_crawl + CRAWL_DELAY - now
        if stall > 0:
          print 'urlopen stalling for %.1f seconds to obey robots.txt' % stall
          time.sleep(stall)

      print 'Opening %s ...' % url
      sys.stdout.flush()
      lines = list( urllib2.urlopen(url, timeout=TIMEOUT) )
      last_crawl = time.time()
      return lines
    except Exception:
      pass

  print 'ERROR: Failed to get URL'
  raise URLError()
