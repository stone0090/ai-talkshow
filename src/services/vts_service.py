import asyncio
import json
import os
import re
import random
import pyvts

from datetime import datetime, timedelta
from pyvts import vts_request
from src.utils.logger import logger_manager


class VTSService:
    def __init__(self, agent_code: str, server_port: int):
        self.logger = logger_manager.get_logger(f"vts_service.{agent_code}")
        self.agent_code = agent_code
        self.server_port = server_port
        self.token_path = f'tmp/vts_token_{server_port}.txt'
        self.is_authenticated = False
        self.vts = pyvts.vts(port=self.server_port, token_path=self.token_path)
        self.vts.vts_request = vts_request.VTSRequest(
            developer=f'stone',
            plugin_name=f'pyvts_{self.server_port}'
        )


    async def authenticate(self) -> None:
        """认证VTS服务"""
        if self.is_authenticated:
            self.logger.debug(f'VTS already authenticated for port {self.server_port}')
            return
        try:
            self.logger.debug(f'Authenticating VTS for port {self.server_port}')
            authentic_token = None
            try:
                authentic_token = await self.vts.read_token()
                self.logger.debug(f"Reading token from {self.token_path}")
            except Exception as e:
                self.logger.warning(f"Error reading token: {e}")
            if authentic_token is not None:
                self.logger.debug(f"Token exists for port {self.server_port}")
            else:
                self.logger.debug(f'No token found for port {self.server_port}')
                if os.path.exists(self.token_path):
                    os.remove(self.token_path)
                await self.vts.connect()
                self.logger.debug(f'Successfully connected to VTS for port {self.server_port}')
                await self.vts.request_authenticate_token()
                self.logger.debug(f'Successfully requested authentication token for port {self.server_port}')
                await self.vts.write_token()
                self.logger.debug(f'Successfully wrote token to {self.token_path}')
            await self.vts.connect()
            self.logger.debug(f'Successfully connected to VTS for port {self.server_port}')
            await self.vts.request_authenticate()
            self.logger.debug(f'Successfully authenticated VTS for port {self.server_port}')
            self.is_authenticated = True
        except Exception as e:
            self.logger.error(f"Error in VTS authentication: {e}")
            self.vts = None

    async def open_mouth_by_vtt(self, vtt_path: str) -> None:
        duration_ms = self._calculate_mouth_open_duration(vtt_path)
        await self.open_mouth(duration_ms)

    async def open_mouth(self, duration_ms: int) -> None:
        """控制模型张嘴动作

        Args:
            duration_ms: 张嘴持续时间（毫秒）
        """
        try:
            self.logger.info(f'Opening mouth for {duration_ms} ms')
            await self.authenticate()
            start_time = datetime.now()
            interval = timedelta(milliseconds=100)
            duration = timedelta(milliseconds=duration_ms)
            while datetime.now() - start_time < duration:
                await self.vts.request(self.vts.vts_request.requestSetParameterValue("MouthOpen", random.random()))
                await asyncio.sleep(interval.total_seconds())
            self.logger.info(f'Successfully completed mouth movement for {duration_ms} ms')
        except Exception as e:
            self.logger.error(f"Error in mouth movement: {e}")
            raise

    def _calculate_mouth_open_duration(self, vtt_path: str) -> int:
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
                row = json.loads(lines[-1])
                return (row.get('offset', 0) + row.get('duration', 0)) / 10000
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse VTT file as JSON. Falling back to old format.")

            # 如果 JSON 解析失败，回退到旧格式
            time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
            matches = time_pattern.findall(content)

            total_duration = 0
            for start_time, end_time in matches:
                start_seconds = self._time_to_seconds(start_time)
                end_seconds = self._time_to_seconds(end_time)
                total_duration += (end_seconds - start_seconds) * 1000  # 转换为毫秒

            return int(total_duration)
        except Exception as e:
            self.logger.error(f"Error calculating mouth open duration: {str(e)}", exc_info=True)
            return 0

    def _time_to_seconds(self, time_str: str) -> float:
        """
        将时间字符串转换为秒数
        :param time_str: 时间字符串，格式为 HH:MM:SS,mmm
        :return: 秒数
        """
        hours, minutes, seconds_milliseconds = time_str.split(':')
        seconds, milliseconds = seconds_milliseconds.split(',')
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000


async def main():
    vts1 = VTSService("ai1", 8001)
    await vts1.authenticate()
    await vts1.open_mouth(5000)
    await asyncio.sleep(3)
    await vts1.open_mouth(5000)


if __name__ == "__main__":
    asyncio.run(main())
