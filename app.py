from flask import Flask ,render_template, request
import ssl
from werkzeug.utils import secure_filename
from AI_Test import AI_Test
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__) 
@app.route("/",methods=['GET','POST'])
def hello():
    return "HELLO"

@app.route("/test",methods=['GET','POST'])
def t():
    print(request.is_json)
    params = request.get_json()
    print(params)

@app.route('/ai_post',methods=['GET','POST'])
def post():
        path_dir = "../tamjiat_web/public/upload"
        file_list = os.listdir(path_dir)
        name = ""
        print(request.form['file_name'])
        print(request.form['cduuid'])
        
        lists = request.form['file_name']
        uuid = request.form['cduuid']

        for i in file_list:
            if i == lists:
                name = i
        result = AI_Test(path_dir+"/"+ name)
        db= pymysql.connect(host=os.environ.get("DB_host"),
                     port=int(os.environ.get("DB_port")),
                     user=os.environ.get("DB_user"),
                     passwd=os.environ.get("DB_password"),
                     db=os.environ.get("DB_database"),
                     charset='utf8')
        cursor = db.cursor()
        if result=="정상":
            sql = "UPDATE userDcrop SET AICheck = '완료' , cdName = '"+result+"', iscdCheck='false' where cduuid = '"+uuid+"'"
        else:
            sql = "UPDATE userDcrop SET AICheck = '완료' , cdName = '"+result+"', iscdCheck='true' where cduuid = '"+uuid+"'"
        cursor.execute(sql)
        db.commit()
        db.close()
        return result
    

if __name__ == '__main__':
    ssl_context= ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='server.crt',keyfile='server.key.origin',password='qwerty12')
    app.run(host='192.168.0.23',port=5000,debug=True,ssl_context=ssl_context)