#!/bin/bash

# 定义当前工作目录变量
CURRENT_DIR=$(pwd)
echo "当前目录为：$(pwd)"
if [ "$(basename "$CURRENT_DIR")" = "scripts" ]; then
    cd ..
    echo "切换到上一级目录：$(pwd)"
fi

# 设置环境变量
export PYTHONPATH=$(pwd)

# 创建必要的目录
mkdir -p log tmp

# 启动程序
python src/main.py