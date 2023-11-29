from datetime import datetime


def get_time_seconds(time_str):
    time_format = '%H:%M:%S.%f'
    time_obj = datetime.strptime(time_str, time_format)
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6
