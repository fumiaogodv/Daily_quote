docker-compose.yml
```
version: "3.9"

services:
  quotes:
    image: 0424godv/quotes_prod:latest 
    container_name: quotes_app
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```
# python运行：
### 下载requirements.txt需要的依赖文件
### 运行app.py

# docker:
拉取：`docker pull 0424godv/quotes_prod:latest `
复制docker-compose.yml到本地然后`docker compose up -d`
