import datetime

def format_timestamp(timestamp):
  if timestamp is not None:
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    # Convert from MSD to PDT.
    # Unfortunately some timestamps are in MSK and some in MSD.
    # Also the timestamps are completely broken--their meaning is unknown.
    # The number here gives the correct result, but I don't know why.
    dt = dt - datetime.timedelta(hours=17)
    return dt.strftime('%a %b %d %H:%M PDT')
  else:
    return 'unknown'
