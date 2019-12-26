from flask import Blueprint
# 创建蓝图对象
clazz=Blueprint("clazz",__name__,url_prefix="/clazz/")

# 导入视图模块  是为了初始化整个视图模块里的所有视图函数
from . import views
