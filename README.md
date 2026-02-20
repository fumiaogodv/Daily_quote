

---

# Quotes App 使用说明

## 📥 下载与部署

### 方法一：Python 源码运行

1. **安装依赖**：
下载项目中的 `requirements.txt`，并在终端运行：
```bash
pip install -r requirements.txt

```


2. **设置环境变量（可选）**：
默认账号为 `admin`，密码为 `password`。如需修改，请在运行前设置环境变量 `ADMIN_USER` 和 `ADMIN_PASS`。
3. **启动应用**：
```bash
python app.py

```



### 方法二：Docker 部署（推荐）

1. **拉取镜像**：
```bash
docker pull 0424godv/quotes_prod:latest

```


2. **创建配置文件**：
在本地创建一个名为 `docker-compose.yml` 的文件，并写入以下内容。**请在此文件中直接修改账号和密码**。
```yaml
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
      # --- 账号密码配置 ---
      - ADMIN_USER=admin           # 请修改为你想要的后台账号
      - ADMIN_PASS=123456          # 请修改为你想要的后台密码
      # --- 安全配置 ---
      - FLASK_SECRET_KEY=change_me_to_random_string  # 请随意修改为一串随机字符，用于加密登录状态
    restart: unless-stopped

```


3. **启动容器**：
在 `docker-compose.yml` 所在目录下运行：
```bash
docker compose up -d

```



---

## 🚀 使用说明

### 1. 访问主页

在浏览器访问 `http://localhost:5000` 即可看到语录展示页面。

### 2. 后台管理

在浏览器访问 `http://localhost:5000/admin`。

* 系统会跳转至登录页面，请输入你在 `docker-compose.yml` 中设置的 **ADMIN_USER** 和 **ADMIN_PASS**。
* 登录成功后，即可进行语录的**添加**和**删除**操作。
* 点击页面右上角的“退出登录”即可注销管理员状态。

---

### ✨ 配置项说明

* **ADMIN_USER**: 后台登录用户名（默认：admin）
* **ADMIN_PASS**: 后台登录密码（默认：password）
* **FLASK_SECRET_KEY**: Flask 会话加密密钥。为了安全起见，建议随意填写一串复杂的字符（例如：`j8s9d8...`），防止 Session 被伪造。
* **./data:/app/data**: 将容器内的数据库挂载到本地 `data` 目录，确保删除容器后数据不丢失。
