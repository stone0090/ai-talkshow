#!/bin/bash

# 查找并终止Python进程
pkill -f "python src/main.py"

# 清理临时文件
rm -rf tmp/*.mp3 tmp/*.vtt 