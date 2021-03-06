import sys
import time
import urllib2


class URLError(Exception):
  pass

class URLError404(URLError):
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
          sys.stdout.flush()
          time.sleep(stall)

      print 'Opening %s ...' % url
      sys.stdout.flush()
      last_crawl = time.time()
      lines = list( urllib2.urlopen(url, timeout=TIMEOUT) )
      return lines
    except urllib2.HTTPError, e:
      if e.code == 404:
        print 'ERROR: HTTP 404'
        raise URLError404()
      else:
        pass
    except Exception:
      pass

  print 'ERROR: Failed to get URL'
  raise URLError()
