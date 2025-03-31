import flask
from flask import Flask,request,render_template,Response
import pymysql

app = Flask(__name__,
            static_url_path='/static',#静态文件路径
            static_folder='static',
            template_folder='templates'#模板文件
            )

@app.route('/loginprocess',methods=['POST'])
def process():

    username = request.form.get('uname')
    password = request.form.get('passwd')
    print(username,password)

    # 打开数据库
    db = pymysql.connect(host='localhost',user='root',passwd='root',db='test')
    # 创建游标对象
    cursor = db.cursor()
    # sql语句
    sql = "select * from table1"
    # 执行sql语句
    cursor.execute(sql)
    # 确认
    db.commit()
    list1=[]
    for temp in cursor.fetchall():
        dict = {'name':temp[1],'pass':temp[2]}
        list1.append(dict)
    print(list1)

    for i in list1:
        if(username == i['name'] and password == i['pass']):
            db.close()
            response=flask.make_response("登陆成功")
            response.set_cookie('login', '1', max_age=36000)
            return response

    response = flask.make_response("登录失败,请访问login页面重新登录")
    db.close()
    return response

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/',methods=['GET'])
def index():
    login = request.cookies.get('login')
    if login=='1':
        if request.method=='GET':
            id = request.args.get('id')
            if id==None:
                return render_template('index0.html')
            else:
                # 打开数据库
                db = pymysql.connect(host='localhost', user='root', passwd='root', db='test')
                # 创建游标对象
                cursor = db.cursor()
                # sql语句
                sql = "select * from table1 where id=%s"%(id)
                # 执行sql语句
                cursor.execute(sql)
                # 确认
                db.commit()

                list1 = []
                for temp in cursor.fetchall():
                    dict = {'name': temp[1], 'pass': temp[2]}
                    list1.append(dict)
                return render_template('index.html',id=id,dict=dict)

    else:
        response = flask.make_response('注意：未授权的访问！请访问login页面')
        return response

@app.errorhandler(404)
def page_not_found(error):
    return '你出错了',404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888, debug=True)