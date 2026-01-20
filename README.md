docker-compose.yml
```
version: "3.9"

services:
  quotes:
    # ❗ 必须使用你在 Docker Hub 上的完整镜像名，否则 Docker 会去本地找
    image: 0424godv/quotes_prod:latest 
    container_name: quotes_app
    ports:
      - "5000:5000"
    volumes:
      # ❗ 确保服务器上有 ./data 文件夹，或者 Docker 会自动创建一个
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```
