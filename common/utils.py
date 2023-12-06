import re
from datetime import datetime


def get_time_seconds(time_str):
    time_format = '%H:%M:%S.%f'
    time_obj = datetime.strptime(time_str, time_format)
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6


def parse_webvtt(file_path):
    subtitles = []
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if pattern.match(line):
                # Found timestamp line
                start_time, end_time = pattern.search(line).groups()
                start_time = convert_to_seconds(start_time)
                end_time = convert_to_seconds(end_time)
                subtitles.append({
                    'start_time': start_time,
                    'end_time': end_time
                })
    return subtitles


def convert_to_seconds(timestamp):
    h, m, s = map(float, timestamp.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s


def calculate_duration(subtitles):
    total_duration = 0
    for subtitle in subtitles:
        duration = subtitle['end_time'] - subtitle['start_time']
        total_duration += duration
    return total_duration * 1000


if __name__ == "__main__":
    subtitles = parse_webvtt('../tmp/ai2.vtt')
    total_duration = calculate_duration(subtitles)
    print(f'Total duration of subtitles: {total_duration:.3f} seconds')
