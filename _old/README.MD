# AI Talkshow

## 项目简介

AI Talkshow 是一个创新性的直播间项目，旨在通过两个 AI
聊天进行实时对话，为观众提供独特而有趣的体验。这个项目结合了人工智能和实时互动，展示了机器之间的交流和讨论，同时也探索了人工智能领域的新可能性。

## 功能特性

- **实时对话：** 两个 AI 将在直播间进行实时对话，呈现出生动有趣的互动场面。
- **观众互动：** 观众可以通过聊天室与 AI 进行互动，提出问题或建议。
- **开放源代码：** 项目代码完全开放，欢迎开发者贡献和提出改进建议。

## 效果演示

![](ai_talkshow_demo.png)

## 运行环境

### 安装 minioconda，并新建一个 python 3.8 环境

### 安装 python 依赖库

`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host https://mirrors.aliyun.com`

### 下载模型 chatglm3-6b 和 qwen2-7b-instruct
https://modelscope.cn/models/ZhipuAI/chatglm3-6b
https://modelscope.cn/models/qwen/Qwen2-7B-Instruct

### 测试 tts 文字转语音在线服务

`python commont/tts.py`

### 安装 VTubeStudio

https://denchisoft.com/

## 运行项目

根据实际情况调整配置文件`config.py`。

### 启动AI聊天服务

`sh start.sh`

包含以下命令
`python -m http.server`
`python common/subtitle.py -path tmp/ai1.vtt -port 8765`
`python common/subtitle.py -path tmp/ai2.vtt -port 8766`
`python ai_talkshow.py`

### 启动本地大模型（待开发）

`python chatglm/openai_api.py`
`python chatqwen/openai_api.py`

### 启动B站弹幕监听服务（待开发）

`python blivedm/server.py`