import pytz
from datetime import datetime

def time_now():
    tz = pytz.timezone('Europe/Kiev')  # Заменить на свой нужный часовой пояс
    return datetime.now(tz)