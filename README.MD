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

### 安装 python（建议3.8.10或以上）

https://www.python.org/downloads/release/python-3810/

### 安装 python 依赖库

`pip install -r requirements.txt`

### 下载 ChatGLM3-6B 模型

https://modelscope.cn/models/ZhipuAI/chatglm3-6b/summary

### 申请通义千问在线服务 api_key

https://dashscope.aliyun.com/

### 测试 tts 文字转语音在线服务

`python tts.py`

### 安装 VTubeStudio

https://denchisoft.com/

## 运行项目

根据实际情况调整配置文件`config.py`。

### 启动B站弹幕监听服务（待开发）

`python blivedm/server.py`

### 启动chatglm服务

`python chatglm/openai_api.py`

### 把项目发布成静态网站

`python -m http.server`

### 运行字幕服务器（依赖项目发布成静态网站）

`python common/subtitle.py -path tmp/ai1.vtt -port 8765`
`http://localhost:8000/common/subtitle.html?serverPort=8765`

### 运行字幕服务器（依赖项目发布成静态网站）

`python common/subtitle.py -path tmp/ai2.vtt -port 8766`
`http://localhost:8000/common/subtitle.html?serverPort=8766`

### 启动AI聊天服务

`python ai_talkshow.py`