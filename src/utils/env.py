import os

# 获取所有环境变量
env_vars = os.environ

# 打印所有环境变量
for key, value in env_vars.items():
    print(f"{key}: {value}")