import re
import json
from src.utils.logger import logger_manager

logger = logger_manager.get_logger(f"subtitle")


def calculate_mouth_open_duration(vtt_path: str) -> int:
    """
    根据 .vtt 文件计算张嘴的持续时间
    :param vtt_path: .vtt 文件路径
    :return: 张嘴的持续时间（毫秒）
    """
    try:
        with open(vtt_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 尝试解析 JSON 数据
        try:
            lines = content.strip().split('\n')
            total_duration = sum(
                json.loads(line).get('duration', 0)
                for line in lines
                if line.startswith('{"type": "WordBoundary"')
            )
            return int(total_duration / 10000)
        except json.JSONDecodeError:
            logger.warning("Failed to parse VTT file as JSON. Falling back to old format.")

        # 如果 JSON 解析失败，回退到旧格式
        time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
        matches = time_pattern.findall(content)

        total_duration = 0
        for start_time, end_time in matches:
            start_seconds = _time_to_seconds(start_time)
            end_seconds = _time_to_seconds(end_time)
            total_duration += (end_seconds - start_seconds) * 1000  # 转换为毫秒

        return int(total_duration)
    except Exception as e:
        logger.error(f"Error calculating mouth open duration: {str(e)}", exc_info=True)
        return 0


def _time_to_seconds(time_str: str) -> float:
    """
    将时间字符串转换为秒数
    :param time_str: 时间字符串，格式为 HH:MM:SS,mmm
    :return: 秒数
    """
    hours, minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
