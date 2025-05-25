import subprocess


def start_static_server(port="8080", root="./src/static"):
    try:
        process = subprocess.Popen(
            ["python", "-m", "http.server", port, "--directory", root],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("静态文件服务器已启动: http://localhost:8000")
        return process
    except Exception as e:
        print(f"启动静态服务器失败: {e}")
        return None


if __name__ == "__main__":
    # 启动静态文件服务器
    static_server = start_static_server("8080", "../src/static")
    if not static_server:
        raise RuntimeError("无法启动静态文件服务器")
    # 可选：退出时终止静态服务器
    static_server.terminate()
    static_server.wait()
    print("静态文件服务器已关闭")
