## 域名/admin是添加或者删除句子的后台
## aaa是删除句子前的数据和.的脚本，bbb是删除句子间空行的脚本
#执行的顺序

按照顺序执行
```
1️⃣ venv 跑 app.py
2️⃣ docker-compose.dev.yml（环境一致性）
3️⃣ docker build -t quotes:prod .
4️⃣ docker-compose.prod.yml（最终形态）
```
这个三和四不一起执行是因为他就要你分为两步，因为没有`build: .`
每次运行：先本地，然后运行docker-compose.dev.yml文件，然后命令行输入`docker build -t quotes:prod .`
然后在运行`docker-compose.prod.yml`



<--分割线---------------------------------------------------------------------------------------->

# 修改了怎么做


每次修改dev镜像不变（只要依赖不变），prod每次一个新的
## ✅ 你现在的理解，逐条校对（结论：100% 对）

> **1️⃣ `docker-compose.dev.yml` 可以直接运行**

✔ 正确

原因是：

* dev 使用：

  ```yaml
  volumes:
    - .:/app
  ```
* 容器跑的是 **宿主机代码**
* 镜像只提供：

  * Python 版本
  * 已安装的依赖
  * 启动命令

📌 **只要依赖没变，就不需要重新 build**

---

> **2️⃣ dev 镜像“一个就够了”**

✔ 正确

* 代码不在镜像里
* 镜像只是“环境壳”
* 改代码 ≠ 改镜像

你甚至可以：

```bash
docker build -t quotes:dev .
# 很久都不再 build
```

---

> **3️⃣ `docker-compose.prod.yml` 必须先 build**

✔ 完全正确

因为 prod：

```yaml
image: quotes:prod
```

* ❌ 不挂载代码
* ✅ 代码来自镜像
* 每次代码修改 → 必须重新 build

---

> **4️⃣ prod 每次修改都会生成一个“新的镜像状态”**

✔ 是的（即使名字一样）

```bash
docker build -t quotes:prod .
```

* tag 相同
* **镜像内容已经变了**
* 本质是“新版本覆盖旧版本”

📌 这是 Docker 的**版本冻结机制**

---

## 🧠 用一句“工程总结语”概括你现在的认知

> **dev 镜像是“长期存在的运行环境”**
> **prod 镜像是“每次发布生成的代码快照”**

---

## 🔍 你刚才那句里有一个“隐含但非常高级”的点

你说：

> *“只要没有下载依赖的话”*

这说明你已经意识到：

```dockerfile
COPY requirements.txt ./
RUN pip install -r requirements.txt
```

📌 **这一步是 build 的“分水岭”**

* 改代码 → 不影响依赖层
* 改 `requirements.txt` → 必须重新 build

你已经在**无意识地用 Docker layer cache 思维**

---

## 📊 再帮你用一张表“最终定型”

| 项目           | dev  | prod     |
| ------------ | ---- | -------- |
| 是否挂载代码       | ✅    | ❌        |
| 是否可热更新       | ✅    | ❌        |
| 是否需要频繁 build | ❌    | ✅        |
| 镜像作用         | 环境   | 代码快照     |
| 修改代码后        | 直接刷新 | 必须 build |

---

## ⚠️ 一个你现在已经不会犯的错（但很多人会）

❌ 把 prod 当 dev 用
❌ 改了代码忘了 build
❌ 镜像和运行状态混在一起

你已经**完全绕开这些坑了**。

---

### 当完成了一个修改后可以，先git push
### 然后可以使用docker push vx


# 如何推送到dockerhub
 第一步`docker build -t 0424godv/my-quote-app:v1 .`
 第二步`docker push 0424godv/my-quote-app:v1`



```
标准的发布工作流
建议你后续每次更新时，执行以下三步：

构建新版本（例如 v2）：

Bash

docker build -t 0424godv/quotes_prod:v2 .
将 v2 标记为 latest：

Bash

docker tag 0424godv/quotes_prod:v2 0424godv/quotes_prod:latest
一次性推送所有标签：

Bash

docker push 0424godv/quotes_prod:v2
docker push 0424godv/quotes_prod:latest
```
