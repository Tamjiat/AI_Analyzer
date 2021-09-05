from flask import Flask ,render_template, request
from werkzeug.utils import secure_filename
from AI_Test import AI_Test
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__) 

@app.route('/test_post',methods=['GET','POST'])
def post():
    if request.method=='POST':
        path_dir = "../tamjiat_web/public/upload"
        file_list = os.listdir(path_dir)
        name = ""
        lists = request.args['file_name']
        uuid = request.args['cduuid']
        print(lists)
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
        sql = "UPDATE userDcrop SET AICheck = '완료' , cdName = '"+result+"', iscdCheck='true' where cduuid = '"+uuid+"'"
        cursor.execute(sql)
        db.commit()
        db.close()
        return result
    

if __name__ == '__main__':
    app.run(host='192.168.0.23',port=5000,debug=True)