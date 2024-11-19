# 使用官方 Python 映像作為基礎
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# 複製需要的文件
COPY requirements.txt .
COPY "Cash & Chill.py" .
COPY screenshots/ ./screenshots/

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變數
ENV DISPLAY=:0

# 運行應用
CMD ["python", "Cash & Chill.py"] 