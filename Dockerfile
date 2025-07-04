FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y build-essential

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 启动命令（Fly 会识别）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
