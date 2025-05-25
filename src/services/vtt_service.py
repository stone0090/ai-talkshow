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
        self._start()

    async def send_subtitle_by_text(self, text: str):
        if not self.websocket:
            self.logger.warning(f"send_text failed, websocket is None!")
            return
        try:
            await self.websocket.send(json.dumps({
                "text": text,
                "class": "online"
            }, ensure_ascii=False))
        except Exception as e:
            self.logger.error(f"Failed to send text: {e}")

    async def send_subtitle_by_vtt(self, file_path: str):
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

            merged_entries = self._merge_entries(entries)
            self.logger.debug(f"merged_entries: {str(merged_entries)}")
            merged_entries_count = len(merged_entries)
            previous_offset = None
            for i in range(merged_entries_count):
                self.logger.debug(f"for i in range(merged_entries_count): {i}")
                entry = merged_entries[i]
                text = entry.get('text')
                offset = entry.get('offset', 0) / 10_000_000  # 转换为秒
                duration = entry.get('duration', 0) / 10_000_000  # 转换为秒
                if not text:
                    continue
                sleep_seconds = offset if i == 0 else (offset - previous_offset)
                send_data = json.dumps({
                    "text": text,
                    "class": "online"
                }, ensure_ascii=False)
                self.logger.info(f"已推送: {send_data} (延迟 {sleep_seconds:.2f}s)")
                await asyncio.sleep(sleep_seconds)
                await self.websocket.send(send_data)
                if i == merged_entries_count - 1:
                    await asyncio.sleep(duration)
                    await self.websocket.send(json.dumps({
                        "text": text,
                        "class": "offline"
                    }, ensure_ascii=False))
                previous_offset = offset
        except Exception as e:
            self.logger.error(f"推送 vtt 文件失败: {e}", exc_info=True)

    @staticmethod
    def _merge_entries(entries, merge_size=10):
        merged_entries = []
        for i in range(0, len(entries), merge_size):
            merged_entry = {
                "text": " ".join([entry["text"] for entry in entries[i:i + merge_size]]),
                "offset": entries[i]["offset"],
                "duration": sum(entry["duration"] for entry in entries[i:i + merge_size]),
            }
            merged_entries.append(merged_entry)
        return merged_entries

    async def _watch(self, websocket):
        self.logger.info(f"watch start...")
        async for message in websocket:
            self.logger.info(f"watch message: {message}")
            if message == "success":
                self.logger.info(f"WebSocket client connected to port {self.server_port}")
                self.websocket = websocket
        self.logger.info(f"watch end...")

    async def _start_websocket(self):
        async with websockets.serve(self._watch, "0.0.0.0", self.server_port):
            self.logger.info(f"WebSocket server started on port {self.server_port}")
            await asyncio.Future()

    def _start(self):
        """启动 WebSocket 服务并在后台线程运行"""
        if self.thread and self.thread.is_alive():
            self.logger.warning("WebSocket server is already running.")
            return

        self.loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._start_websocket())

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()
        time.sleep(0.5)


if __name__ == "__main__":
    vtt_service1 = VTTService("ai1", 9001)
    print("需要用debug卡住，要等 websocket client 连上之后再继续")
    asyncio.run_coroutine_threadsafe(vtt_service1.send_subtitle_by_vtt("log/ai1.vtt"), vtt_service1.loop)
    print("需要用debug卡住")
