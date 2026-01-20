FROM python:3

WORKDIR /app

# 升级 pip 并安装依赖
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 设置 Flask 环境变量（让 Flask 知道运行哪个文件，并允许外部访问）
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 运行 Flask 开发服务器（默认端口 5000）
CMD ["flask", "run", "--port", "5000"]