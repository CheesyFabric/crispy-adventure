from flask import Flask,render_template
from apps import config
# 创建app对象
app=Flask(__name__)

# 导入config.py里的键值对
app.config.from_object(config)

# 导入stu蓝图对象
from apps.stu import stu
from apps.qd import qd
# 注册蓝图 相当于把stu蓝图对象和app对象绑定 这样app初始化是蓝图对象也可以初始化
app.register_blueprint(stu)
app.register_blueprint(qd)

from apps import filter
from apps.decorator import login_validate
@app.route("/home/",endpoint='home')
@login_validate
def home():
    return render_template("home.html")


from flask_wtf.csrf import CSRFProtect

CSRFProtect(app)