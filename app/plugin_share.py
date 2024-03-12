from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta
import sqlite3
import os

DATABASE = 'database/mydatabase.db'
live_update_configs=True #update configs at each user request, you will not need to restart the program if you make changes but higher I/O usage.
if __name__ == '__main__':
    app_share = Flask(__name__)
else:
    app_share=Blueprint('app_share', __name__)



def read_share_configs(folder_path="share"):
    file_data = []

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 '{folder_path}' 不存在")
        return file_data

    # 遍历文件夹中的文件
    for file_name in os.listdir(folder_path):
        # 确保是txt文件
        if file_name.endswith(".txt") and file_name!="README.txt":
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                # 去掉文件扩展名，只保留文件名
                file_name_no_extension = os.path.splitext(file_name)[0]
                # 读取文件内容并存入嵌套数组
                file_content = file.readlines()
                file_content_res=[]
                for i in file_content:
                    i=i.replace(" ","").replace("\n","")
                    comment=""
                    if i!="":
                        if "#" in i:
                            comment=i[i.find("#")+1:]
                            i=i[:i.find("#")]
                        file_content_res.append([i, comment])
                file_data.append([[file_name_no_extension], file_content_res])

    return file_data


def timestamp_to_datetime(timestamp):
    try:
        timestamp=float(timestamp)
        # Using Python's datetime module to convert timestamp to a readable format
        return str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(f"Error converting timestamp to datetime: {e}")
        return None


def get_latest_messages(keyword):
    try:
        # 连接到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 查询最新的100条记录
        cursor.execute(f'SELECT * FROM messages WHERE content LIKE \'%{keyword}%\' ORDER BY ROWID DESC LIMIT 100;')
        messages = cursor.fetchall()

        # 更新timestamp_to_datetime
        for i in range(len(messages)):
            messages[i] = list(messages[i])
            if len(messages[i]) > 0:
                messages[i][0] = timestamp_to_datetime(messages[i][0])

        conn.close()
        return messages
    except Exception as e:
        # 处理异常情况，可以打印错误信息或者返回一个空列表
        print(f"Error: {e}")
        return []


share_configs=read_share_configs()

@app_share.route('/share/<app>/<key>')
def ui_share(app, key):
    #app = request.args.get('app')
    #key = request.args.get('key')
    if not app or not key:
        return jsonify({"status":False, "detail":"In this share mode,app and key should be provided. Like /share/<app>/<key>"})
    if live_update_configs:
        share_configs=read_share_configs()
    for i in share_configs:
        if app==i[0][0]:
            #print(i)
            for j in i[1]:
                if key==j[0] and key!=i[1][0][0]:
                    #print(i[1][0])
                    messages = get_latest_messages(keyword=i[1][0][0])
                    return render_template('messages.html', messages=messages)
            return jsonify({"status":False, "detail":f"Invalid key for app {app}. Contact with administrator or try again later."})
        else:
            #print(app,i[0])
            pass
    return jsonify({"status":False, "detail":f"Invalid app {app}. Contact with administrator or try again later."})
   
    
    
@app_share.route('/get_url')
def get_url():
    if live_update_configs:
        share_configs=read_share_configs()
    return render_template('get_url.html', share_configs=share_configs)

