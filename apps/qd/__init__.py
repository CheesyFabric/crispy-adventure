from flask import Blueprint
# 创建蓝图对象
qd=Blueprint("qd",__name__,url_prefix="/qd")

# 导入视图模块  是为了初始化整个视图模块里的所有视图函数
from . import views

