import asyncio
import websockets
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import get_time_seconds


class Subtitles:
    def __init__(self, vtt_path, server_port):
        self.vtt_path = vtt_path
        self.server_port = server_port
        self.websocket = None

    async def serve(self, websocket):
        subtitles = await parse_webvtt(self.vtt_path)
        await send_subtitles(websocket, subtitles)
        await self.watch(websocket)

    async def watch(self, websocket):
        event_handler = SubtitleFileHandler(websocket, self.vtt_path)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            observer.stop()
        observer.join()

    def start(self):
        start_server = websockets.serve(self.serve, 'localhost', self.server_port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


class SubtitleFileHandler(FileSystemEventHandler):
    def __init__(self, websocket, file_path):
        self.websocket = websocket
        self.file_path = file_path
        self.event_deduplication = 0

    def on_modified(self, event):
        # 事件去重
        self.event_deduplication = self.event_deduplication + 1
        if self.event_deduplication % 2 == 0:
            self.event_deduplication = 0
            return
        if event.src_path.endswith(self.file_path):
            asyncio.run(update_subtitles(self.websocket, self.file_path))


async def update_subtitles(websocket, file_path):
    subtitles = await parse_webvtt(file_path)
    await send_subtitles(websocket, subtitles)


async def send_subtitles(websocket, subtitles):
    print('send_subtitles start...')
    last_start = 0
    for subtitle in subtitles:
        current_start = get_time_seconds(subtitle['start'])
        seconds = current_start - last_start
        last_start = current_start
        print(seconds)
        await asyncio.sleep(seconds)
        await websocket.send(subtitle['text'])
    print('send_subtitles end...')


async def parse_webvtt(vtt_path):
    subtitles = []
    with open(vtt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        cue = None
        for line in lines:
            line = line.strip()
            if line and not line.startswith('WEBVTT'):
                if re.match(r'\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+', line):
                    if cue:
                        subtitles.append(cue)
                    cue = {'start': line.split(' --> ')[0], 'text': ''}
                else:
                    if cue is not None:
                        cue['text'] += line + ' '
        if cue:
            subtitles.append(cue)
    return subtitles


if __name__ == "__main__":
    service = Subtitles("tmp/tts_glm.vtt", 8765)
    service.start()
