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