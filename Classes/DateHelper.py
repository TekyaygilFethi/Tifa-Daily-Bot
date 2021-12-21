from datetime import datetime, timedelta
from dateutil.parser import parse

class DateHelper():
    @staticmethod
    def GetFormattedToday():
        return datetime.now().strftime("%m.%d.%Y %H:%M:%S")

    @staticmethod
    def ParseDate(date):
        today = datetime.now()

        try:
            day_interval = eval(date)
            if day_interval > 0:
                day_interval *= -1
            date = today + timedelta(days=day_interval)
        except:
            date = date.replace('(', '').replace(')', '').replace('T',' ')
            date = parse(date)

        if date.hour == 0 and date.minute == 0 and date.second == 0:
            date = date.replace(hour=today.hour, minute=today.minute, second=today.second)

        return date.strftime("%m.%d.%Y %H:%M:%S")