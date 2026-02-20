from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import hashlib
from functools import wraps  # 用于创建装饰器
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # 这行代码会允许所有域名的跨域请求

# --- 1. 配置部分 (修改) ---
db_path = os.path.join(os.getcwd(), 'data', 'quotes.db')
if not os.path.exists('data'):
    os.makedirs('data')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# [关键] 设置密钥，用于加密 Session。必须设置！
# 优先从环境变量获取，如果没有则使用默认值（仅用于测试，生产环境请在 Docker 里设置）
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-dev-secret-key')

# [关键] 获取管理员账号密码
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'password')

db = SQLAlchemy(app)


# 2. 数据模型 (保持不变)
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 3. 初始化数据库 (保持不变)
with app.app_context():
    db.create_all()
    if Quote.query.count() == 0:
        file_path = 'aaa.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                for line in lines:
                    db.session.add(Quote(content=line))
                db.session.commit()


# --- [新增] 登录验证装饰器 ---
# 这个函数会检查用户是否登录，如果没有登录，就踢回登录页
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# --- 路由部分 ---

@app.route('/')
def index_page():
    return render_template('index.html')


# --- [新增] 登录与登出路由 ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证账号密码
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            # 如果有 next 参数（比如原本想访问 admin），登录后跳转过去，否则去 admin
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin'))
        else:
            flash('账号或密码错误，请重试')  # 需要在 html 里显示这个消息

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# --- API 接口 (保持不变) ---

@app.route('/api/daily')
def get_daily_quote():
    total = Quote.query.count()
    if total == 0:
        return jsonify({"error": "数据库中暂无语录"})
    today = date.today().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    offset = seed % total
    quote = Quote.query.offset(offset).limit(1).first()
    return jsonify({"id": quote.id, "content": quote.content})


@app.route('/quotes')
def get_all_quotes():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return jsonify([{
        "id": q.id,
        "content": q.content,
        "time": q.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for q in quotes])


# --- 管理路由 (加上 @login_required 保护) ---

# 注意：这里加上了 @login_required
@app.route("/admin")
@login_required
def admin():
    quotes = Quote.query.order_by(Quote.id.desc()).all()
    return render_template("admin.html", quotes=quotes)


# 这里也加，防止有人直接发 POST 请求攻击
@app.route("/admin/add", methods=["POST"])
@login_required
def admin_add():
    text = request.form.get("text", "")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        db.session.add(Quote(content=line))
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:quote_id>")
@login_required
def admin_delete(quote_id):
    q = Quote.query.get_or_404(quote_id)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin"))


# 原有的 delete 接口如果也想保护，请加上装饰器
@app.route('/delete/<int:quote_id>')
@login_required
def delete_quote(quote_id):
    quote = Quote.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return f"ID {quote_id} 已删除"
    return "未找到对应内容", 404


# 这是一个特例：原本的 add_quote 看起来是给脚本用的
# 如果你想保留公开提交（不需要密码），就不要加装饰器。
# 如果你想这个也必须管理员才能提交，加上 @login_required
@app.route('/add_quote', methods=['POST', 'GET'])
# @login_required  <-- 根据你的需求决定是否开启
def add_quote():
    content = request.args.get('text')
    if not content: return "请提供 text 参数", 400
    new_item = Quote(content=content)
    db.session.add(new_item)
    db.session.commit()
    return f"内容已存入数据库，ID 为: {new_item.id}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)