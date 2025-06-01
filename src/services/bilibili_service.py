import asyncio
import http.cookies
from typing import Optional, Callable, Dict, Any
import aiohttp
from src import blivedm
import src.blivedm.models.web as web_models
from src.utils.logger import logger_manager


class BilibiliService:
    def __init__(self, config: dict):
        self.logger = logger_manager.get_logger("bilibili_service")
        self.logger.debug(f"Initializing debate manager with config: {config}")
        self.config = config
        self.room_id = config.get("live_room_id")
        self.session_data = config.get("session_data")
        self.session: Optional[aiohttp.ClientSession] = None
        self.client = None
        self.handler = None
        self.danmaku_queue = asyncio.Queue()

    async def initialize(self):
        """Initialize the Bilibili service with session"""
        cookies = http.cookies.SimpleCookie()
        cookies['SESSDATA'] = self.session_data
        cookies['SESSDATA']['domain'] = 'bilibili.com'
        self.session = aiohttp.ClientSession()
        self.session.cookie_jar.update_cookies(cookies)
        self.client = blivedm.BLiveClient(self.room_id, session=self.session)
        self.handler = BilibiliHandler(self.handle_danmaku)
        self.client.set_handler(self.handler)

    async def start(self):
        """Start monitoring the live stream"""
        if not self.client:
            await self.initialize()
        self.client.start()
        self.logger.info(f"Started monitoring room {self.room_id}")

    async def stop(self):
        """Stop monitoring the live stream"""
        if self.client:
            await self.client.stop_and_close()
        if self.session:
            await self.session.close()
        self.logger.info(f"Stopped monitoring room {self.room_id}")

    def handle_danmaku(self, username: str, message: str):
        """Handle incoming danmaku messages"""
        asyncio.create_task(self.danmaku_queue.put((username, message)))
        # 打印danmaku_queue的大小
        self.logger.debug(f"danmaku_queue size: {self.danmaku_queue.qsize()}")

    def get_danmaku_queue(self):
        return self.danmaku_queue


class BilibiliHandler(blivedm.BaseHandler):
    def __init__(self, danmaku_callback: Optional[Callable[[str, str], None]] = None):
        self.logger = logger_manager.get_logger("bilibili_handler")
        self.danmaku_callback = danmaku_callback

    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        """Handle incoming danmaku messages"""
        if self.danmaku_callback:
            self.danmaku_callback(message.uname, message.msg)
        self.logger.debug(f"Received danmaku from {message.uname}: {message.msg}")

    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        """Handle heartbeat messages"""
        self.logger.debug(f"Heartbeat from room {client.room_id}")

    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        """Handle gift messages"""
        self.logger.info(f"Gift from {message.uname}: {message.gift_name}x{message.num}")

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        """Handle super chat messages"""
        self.logger.info(f"Super chat from {message.uname}: {message.message}")
