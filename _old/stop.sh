#!/bin/bash

# 检测操作系统类型
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then

    pkill -f "python ai_talkshow.py"
    echo "ai_talkshow.py 服务已停止"

    pkill -f "python -m http.server"
    echo "Python HTTP 服务器已停止"

    pkill -f "python common/subtitle.py -path tmp/ai1.vtt -port 8765"
    echo "subtitle.py (端口 8765) 服务已停止"

    pkill -f "python common/subtitle.py -path tmp/ai2.vtt -port 8766"
    echo "subtitle.py (端口 8766) 服务已停止"

elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then

    start powershell -NoExit -Command "taskkill /F /IM python.exe; exit;"

else
    echo "无法识别的操作系统类型"
fi

echo "所有服务已停止"
