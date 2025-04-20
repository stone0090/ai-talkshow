import argparse
import asyncio
import json
import os

import websockets
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import get_time_seconds


class Subtitle:
    def __init__(self, file_path, server_port):
        self.file_path = file_path
        self.server_port = server_port
        self.websocket = None

    async def serve(self, websocket):
        print('serve start...')
        subtitles = await parse_subtitle(self.file_path)
        print('serve subtitles:' + str(subtitles))
        await send_subtitle(websocket, subtitles)
        print('serve end...')
        print('\n')
        await self.watch(websocket)

    async def watch(self, websocket):
        event_handler = SubtitleFileHandler(websocket, self.file_path)
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(self.file_path), recursive=False)
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
                print('on_modified update...')
                self.last_file_content = cur_file_content
                asyncio.run(update_subtitle_textbox(self.websocket, self.file_path))
            else:
                print('on_modified no update...')
            print('on_modified end...')
            print('\n')


async def update_subtitle_textbox(websocket, file_path):
    print('update_subtitle_textbox start...')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) <= 0:
            return
        first_line = lines[0]
        print('first_line:' + first_line)
        if re.match(r'1', first_line):
            print('update_subtitle start...')
            subtitles = await parse_subtitle(file_path)
            print('update_subtitle ' + str(subtitles))
            await send_subtitle(websocket, subtitles)
            print('update_subtitle end...')
        if re.match(r'CLASS', first_line):
            print('update_class_name start...')
            class_name = await parse_send_class(websocket, file_path)
            print('update_class_name class_name:' + str(class_name))
            print('update_class_name end...')
    print('update_websocket_data end...')
    print('\n')


async def parse_subtitle(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) <= 0:
            return subtitles
        first_line = lines[0].strip()
        if not re.match(r'1', first_line):
            return subtitles
        cue = None
        for line in lines:
            line = line.strip()
            # 判断字符串转数字，
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
                if cue:
                    subtitles.append(cue)
                cue = {'start': line.split(' --> ')[0], 'text': ''}
            else:
                if cue is not None:
                    cue['text'] += line + ' '
        if cue:
            subtitles.append(cue)
    return subtitles


async def send_subtitle(websocket, subtitles):
    if not subtitles or len(subtitles) == 0:
        return
    print('send_subtitle start...')
    last_start = 0
    for subtitle in subtitles:
        current_start = get_time_seconds(subtitle['start'])
        seconds = current_start - last_start
        last_start = current_start
        print('send_subtitle seconds:' + str(seconds) + ', subtitle:' + subtitle['text'])
        await asyncio.sleep(seconds)
        await websocket.send(json.dumps({"text": subtitle['text']}))
    print('send_subtitle end...')
    print('\n')


async def parse_send_class(websocket, file_path):
    class_name = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) <= 0:
            return class_name
        first_line = lines[0].strip()
        if not re.match(r'CLASS', first_line):
            return class_name
        class_name = lines[1].strip()
    if not class_name == '':
        await websocket.send(json.dumps({"class": class_name}))
    return class_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Subtitle WebSocket Server')
    parser.add_argument('-path', type=str, help='Specify the file path', required=True)
    parser.add_argument('-port', type=int, help='Specify the server port', required=True)
    args = parser.parse_args()
    path = os.path.abspath(args.path)
    port = args.port
    service = Subtitle(path, port)
    service.start()
    print('Server started...path:' + path + 'port:' + str(port))

# # python common/subtitle.py -path tmp/ai2.vtt -port 8766
# if __name__ == "__main__":
#     path = "D:\\stone\\code\\stone0090\\ai-talkshow\\tmp\\ai1.vtt"
#     port = 8766
#     service = Subtitle(path, port)
#     service.start()
#     print('Server started...path:' + path + 'port:' + str(port))