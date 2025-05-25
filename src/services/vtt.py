import asyncio
import json
import os
import threading
import time
import websockets
from src.utils.logger import logger_manager


class VTTService:
    def __init__(self, agent_code: str, server_port: int):
        self.logger = logger_manager.get_logger(f"vtt_service.{agent_code}")
        self.agent_code = agent_code
        self.server_port = server_port
        self.websocket = None
        self.loop = None
        self.thread = None

    async def watch(self, websocket):
        self.logger.info(f"watch start...")
        async for message in websocket:
            self.logger.info(f"watch message: {message}")
            if message == "success":
                self.logger.info(f"WebSocket client connected to port {self.server_port}")
                self.websocket = websocket
        self.logger.info(f"watch end...")

    async def start_websocket(self):
        async with websockets.serve(self.watch, "0.0.0.0", self.server_port):
            self.logger.info(f"WebSocket server started on port {self.server_port}")
            await asyncio.Future()

    def start(self):
        """启动 WebSocket 服务并在后台线程运行"""
        if self.thread and self.thread.is_alive():
            self.logger.warning("WebSocket server is already running.")
            return

        self.loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.start_websocket())

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()
        time.sleep(0.5)

    async def send_text(self, text: str):
        if not self.websocket:
            self.logger.warning(f"send_text failed, websocket is None!")
            return
        try:
            await self.websocket.send(text)
        except Exception as e:
            self.logger.error(f"Failed to send text: {e}")

    async def send_vtt(self, file_path: str):
        if not self.websocket:
            self.logger.warning(f"send_vtt failed, websocket is None!")
            return
        if not os.path.exists(file_path):
            self.logger.warning(f"send_vtt failed, {file_path} is not exist!")
            return
        try:
            entries = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            entries.append(entry)
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"跳过非法 JSON 行: {line} | 错误: {e}")

            previous_offset = None
            for entry in entries:
                text = entry.get('text')
                offset = entry.get('offset', 0) / 10_000_000  # 转换为秒
                duration = entry.get('duration', 0) / 10_000_000  # 转换为秒
                if not text:
                    continue
                if previous_offset is None:
                    sleep_seconds = offset
                else:
                    sleep_seconds = offset - previous_offset
                send_data = json.dumps({
                    "text": text,
                    "class": "online"
                }, ensure_ascii=False)
                self.logger.info(f"已推送: {send_data} (延迟 {sleep_seconds:.2f}s)")
                await asyncio.sleep(sleep_seconds)
                await self.websocket.send(send_data)
                previous_offset = offset
        except Exception as e:
            self.logger.error(f"推送 vtt 文件失败: {e}", exc_info=True)


if __name__ == "__main__":
    vtt_service1 = VTTService("ai1", 9001)
    print("1")
    vtt_service1.start()
    print("2")
    asyncio.run_coroutine_threadsafe(vtt_service1.send_vtt("log/ai1.vtt"), vtt_service1.loop)
    print("3")
