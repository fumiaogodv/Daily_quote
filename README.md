效果预览：
<img width="916" height="332" alt="image" src="https://github.com/user-attachments/assets/b3a932f3-0370-4777-a715-9a4f8be1b27f" />
<img width="2205" height="851" alt="image" src="https://github.com/user-attachments/assets/9b44a0f7-86d5-435d-9db8-30dd672e8930" />

# 下载
## 第一种方法：
## python运行：
### 下载requirements.txt需要的依赖文件
### 运行app.py
## 第二种方法：
## docker:
拉取：`docker pull 0424godv/quotes_prod:latest `
创建docker-compose.yml文件，然后写入：
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
复制docker-compose.yml到本地然后`docker compose up -d`
# 使用
## 登录localhost:5000来访问主页面
## 登录localhost:5000/admin来实现删除句子和添加句子
