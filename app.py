from flask import Flask, jsonify, request,render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import hashlib
from datetime import date

app = Flask(__name__)

# 1. 数据库路径及配置
db_path = os.path.join(os.getcwd(), 'data', 'quotes.db')
if not os.path.exists('data'):
    os.makedirs('data')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 2. 数据模型
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建议使用 utcnow


# 3. 初始化数据库结构
with app.app_context():
    db.create_all()

    # 检查数据库是否为空，如果为空则从 aaa.txt 导入
    if Quote.query.count() == 0:
        file_path = 'aaa.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                # 假设每行是一条语录
                lines = [line.strip() for line in f.readlines() if line.strip()]
                for line in lines:
                    new_quote = Quote(content=line)
                    db.session.add(new_quote)
                db.session.commit()
            print(f"已成功从 {file_path} 导入 {len(lines)} 条语录")


# --- 路由修改部分 ---

@app.route('/')
def index_page():
    # 访问根目录时，返回 HTML 页面
    return render_template('index.html')

@app.route('/api/daily')  # 把你原来的随机逻辑改到这个 API 接口
def get_daily_quote():
    total = Quote.query.count()
    if total == 0:
        return jsonify({"error": "数据库中暂无语录"})

    today = date.today().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    offset = seed % total
    quote = Quote.query.offset(offset).limit(1).first()

    return jsonify({
        "id": quote.id,
        "content": quote.content
    })

# 将原本的 add_user 修改为 add_quote
@app.route('/add_quote', methods=['POST', 'GET'])
def add_quote():
    # 如果是 GET 请求，可以从 URL 参数获取（方便浏览器快速测试）
    # 例如访问：/add_quote?text=天下就没有偶然
    content = request.args.get('text')

    if not content:
        return "请提供 text 参数", 400

    new_item = Quote(content=content)
    db.session.add(new_item)
    db.session.commit()
    return f"内容已存入数据库，ID 为: {new_item.id}"


@app.route("/admin")
def admin():
    quotes = Quote.query.order_by(Quote.id.desc()).all()
    return render_template("admin.html", quotes=quotes)

@app.route("/admin/add", methods=["POST"])
def admin_add():
    text = request.form.get("text", "")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        db.session.add(Quote(content=line))

    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/admin/delete/<int:quote_id>")
def admin_delete(quote_id):
    q = Quote.query.get_or_404(quote_id)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin"))


# 将原本的 get_users 修改为 get_quotes
@app.route('/quotes')
def get_all_quotes():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()  # 按时间倒序
    return jsonify([
        {
            "id": q.id,
            "content": q.content,
            "time": q.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for q in quotes
    ])


# 额外增加一个删除功能（可选，方便管理）
@app.route('/delete/<int:quote_id>')
def delete_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return f"ID {quote_id} 已删除"
    return "未找到对应内容", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)