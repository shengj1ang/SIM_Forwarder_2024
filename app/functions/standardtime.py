import time
from datetime import datetime, timedelta, timezone


class standard_time():
    def __init__(self,timezone):
        self.timezone=timezone
    def get(self):
        td = timedelta(hours=self.timezone)
        tz = timezone(td)
        dt = datetime.fromtimestamp(time.time(), tz)
        dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        return(str(dt))
        

def timestamp_to_datetime(timestamp):
    try:
        timestamp=float(timestamp)
        return str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(f"Error converting timestamp to datetime in functions/standard_time.py=>timestamp_to_datetime: {e}")
        return None

