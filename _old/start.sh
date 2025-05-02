#!/bin/bash

# 检查并创建 log 目录
if [ ! -d "log" ]; then
    mkdir log
    echo "log 目录已创建"
fi

# 启动静态web服务
nohup python -m http.server > log/static_web.log 2>&1 &
echo "静态web 服务已启动"

# 启动ai1的字幕服务
nohup python common/subtitle.py -path tmp/ai1.vtt -port 8765 > log/subtitle_ai1.log 2>&1 &
echo "ai1字幕 服务已启动"

# 启动ai2的字幕服务
nohup python common/subtitle.py -path tmp/ai2.vtt -port 8766 > log/subtitle_ai2.log 2>&1 &
echo "ai2字幕 服务已启动"

# 启动ai对话服务
nohup python ai_talkshow.py > log/ai_talkshow.log 2>&1 &
echo "ai对话 服务已启动"

# 检测操作系统类型
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
  open http://localhost:8000/common/subtitle.html?serverPort=8765
  open http://localhost:8000/common/subtitle.html?serverPort=8766
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  start http://localhost:8000/common/subtitle.html?serverPort=8765
  start http://localhost:8000/common/subtitle.html?serverPort=8766
else
    echo "无法识别的操作系统类型"
fi

echo "所有服务已启动"
