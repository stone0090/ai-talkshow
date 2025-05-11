import os
import asyncio
import random
from datetime import datetime, timedelta
import pyvts
from pyvts import vts_request
from src.utils.logger import logger_manager

class VTSService:
    def __init__(self, agent_code: str, port: int):
        self.logger = logger_manager.get_logger(f"vts_service.{agent_code}")
        self.agent_code = agent_code
        self.port = port
        self.token_path = f'tmp/vts_token_{port}.txt'
        self.tmp_path = "tmp"
        self._ensure_directories()
        self.vts = pyvts.vts(port=self.port, token_path=self.token_path)
        self.vts.vts_request = vts_request.VTSRequest(
            developer=f'stone',
            plugin_name=f'pyvts_{self.port}'
        )

    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
            self.logger.info(f"Created directory: {self.tmp_path}")

    async def _authenticate(self) -> None:
        """认证VTS服务"""
        try:
            self.logger.info(f'Authenticating VTS for port {self.port}')
            authentic_token = None
            try:
                authentic_token = await self.vts.read_token()
            except Exception as e:
                self.logger.error(f"Error reading token: {e}")
            if authentic_token is not None:
                return
            if os.path.exists(self.token_path):
                os.remove(self.token_path)
            await self.vts.connect()
            await self.vts.request_authenticate_token()
            await self.vts.write_token()
            await self.vts.close()
            self.logger.info(f'Successfully authenticated VTS for port {self.port}')
        except Exception as e:
            self.logger.error(f"Error in VTS authentication: {e}")
            raise

    async def open_mouth(self, duration_ms: int) -> None:
        """控制模型张嘴动作
        
        Args:
            duration_ms: 张嘴持续时间（毫秒）
        """
        try:
            self.logger.info(f'Opening mouth for {duration_ms} ms')
            if not os.path.exists(self.token_path):
                await self._authenticate()

            await self.vts.connect()
            await self.vts.read_token()
            await self.vts.request_authenticate()

            start_time = datetime.now()
            interval = timedelta(milliseconds=100)
            duration = timedelta(milliseconds=duration_ms)

            while datetime.now() - start_time < duration:
                await self.vts.request(
                    self.vts.vts_request.requestSetParameterValue("MouthOpen", random.random())
                )
                await asyncio.sleep(interval.total_seconds())

            await self.vts.close()
            self.logger.info(f'Successfully completed mouth movement for {duration_ms} ms')
        except Exception as e:
            self.logger.error(f"Error in mouth movement: {e}")
            raise

async def main():
    """测试函数"""
    vts1 = VTSService("ai1", 8001)
    task1 = asyncio.create_task(vts1.open_mouth(5000))
    await asyncio.gather(task1)
    await asyncio.sleep(3)
    task1 = asyncio.create_task(vts1.open_mouth(5000))
    await asyncio.gather(task1)

if __name__ == "__main__":
    asyncio.run(main())