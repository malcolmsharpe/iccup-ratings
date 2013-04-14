import datetime

def format_timestamp(timestamp):
  if timestamp is not None:
    dt = datetime.datetime.fromtimestamp(timestamp)
    # Convert from MSD to PDT.
    # Unfortunately some timestamps are in MSK and some in MSD.
    dt = dt - datetime.timedelta(hours=12)
    return dt.strftime('%a %b %d %H:%M PDT')
  else:
    return 'unknown'
