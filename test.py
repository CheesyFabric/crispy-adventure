import pymysql
from random import randint
import datetime

def add_data():
    # 连接数据库
    client=pymysql.connect(host='localhost',port=3306,user='root',password='',db="brandnew_project",charset='utf8')
    # 获取游标
    cursor=client.cursor()
    # 创建sql  0 表示自动维护的主键字段
    sql='insert into t_qd values(0,%s,%s,%s,%s,%s,%s,%s)'
    #生成参数
    """
    lb 2
    dc 3
    """
    uid=3
    stage=1
    progress=5
    code_num=0
    bug_num=0
    create_time='2019-10-27'
    remark="无"

    for i in range(100):
        uid=uid
        stage=stage
        progress+=randint(2,15)
        code_num=randint(50,120)
        bug_num=randint(0,15)

        start_day = datetime.datetime.strptime(create_time, '%Y-%m-%d')
        end_day = start_day + datetime.timedelta(days=1)
        create_time = end_day.strftime('%Y-%m-%d')


        args=[uid,stage,progress,code_num,bug_num,create_time,remark+str(i)]
        #     执行sql
        cursor.execute(sql,args)
        #提交事务
        client.commit()

    #关闭游标、连接
    try:
        if cursor:
            cursor.close()
        if client:
            client.close()
    except Exception as e:
        print(e)

# if __name__ == '__main__':
    # add_data()



