
DIALECT = 'mysql'
DRIVER = 'pymysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'brandnew_project'

DB_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME,
                                                                          PORT,
                                                                          DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设置session
import os
SECRET_KEY=os.urandom(24)

WTF_CSRF_SECRET_KEY = os.urandom(16)