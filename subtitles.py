import argparse
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
        observer.schedule(event_handler, path='tmp', recursive=False)
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
        self.last_file_content = None

    def on_modified(self, event):
        print('on_modified event file_path:' + self.file_path + ', src_path:' + str(event.src_path))
        if event.src_path.endswith(self.file_path[4:]):
            print('on_modified start...')
            with open(self.file_path, 'r', encoding='utf-8') as file:
                cur_file_content = file.read()
            if self.last_file_content != cur_file_content:
                print('on_modified update_subtitles...')
                self.last_file_content = cur_file_content
                asyncio.run(update_subtitles(self.websocket, self.file_path))
            else:
                print('on_modified no update...')
            print('on_modified end...')
            print('\n')


async def update_subtitles(websocket, file_path):
    print('update_subtitles start...')
    subtitles = await parse_webvtt(file_path)
    print('update_subtitles subtitles:' + str(subtitles))
    await send_subtitles(websocket, subtitles)
    print('update_subtitles end...')
    print('\n')


async def send_subtitles(websocket, subtitles):
    print('send_subtitles start...')
    last_start = 0
    for subtitle in subtitles:
        current_start = get_time_seconds(subtitle['start'])
        seconds = current_start - last_start
        last_start = current_start
        print('send_subtitles seconds:' + str(seconds) + ', subtitle:' + subtitle['text'])
        await asyncio.sleep(seconds)
        await websocket.send(subtitle['text'])
    print('send_subtitles end...')
    print('\n')


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
    parser = argparse.ArgumentParser(description='Subtitle WebSocket Server')
    parser.add_argument('-path', type=str, help='Specify the vtt path', required=True)
    parser.add_argument('-port', type=int, help='Specify the server port', required=True)
    args = parser.parse_args()
    path = args.path
    port = args.port
    service = Subtitles(path, port)
    service.start()
    print('Server started...path:' + path + 'port:' + str(port))
