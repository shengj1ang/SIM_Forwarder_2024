from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta

import sqlite3
DATABASE = 'database/mydatabase.db'
app_webUI=Blueprint('app_webUI', __name__)
def timestamp_to_datetime(timestamp):
    try:
        timestamp=float(timestamp)
        # Using Python's datetime module to convert timestamp to a readable format
        return str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(f"Error converting timestamp to datetime: {e}")
        return None


def get_latest_messages():
    try:
        # 连接到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 查询最新的100条记录
        cursor.execute('SELECT * FROM messages ORDER BY ROWID DESC LIMIT 100;')
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



@app_webUI.route('/ui/messages')
def ui_messages():
    messages = get_latest_messages()
    return render_template('messages.html', messages=messages)
 



def get_latest_calls():
    try:
        # 连接到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 查询最新的100条记录
        cursor.execute('SELECT * FROM calls ORDER BY ROWID DESC LIMIT 100;')
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



@app_webUI.route('/ui/calls')
def ui_calls():
    calls = get_latest_calls()
    return render_template('calls.html', calls=calls)
    

@app_webUI.route('/myphone')
def ui_index():
    return render_template('index.html')
    
 

def get_latest_baidu_messages():
    try:
        # 连接到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 查询最新的100条记录
        cursor.execute('SELECT * FROM messages WHERE content LIKE \'%百度%\' ORDER BY ROWID DESC LIMIT 100;')
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


share_baidu_key=[
"f1b1b08a", #Default
"443154b9", #User1
"37a52e37", #User2
"46c405a6", #User3
"beab3e29", #User4
"65b7c8c6", #User5
]
@app_webUI.route('/share/baidu')
def ui_share_baidu():
    key = request.args.get('key')
    if not key:
        return jsonify({"status":False, "detail":"In this share mode, a key should be provided. Like /?key=abcdefg"})
    if key not in share_baidu_key:
        return jsonify({"status":False, "detail":"Invalid key for share_baidu. Contact with administrator or try again later."})
    messages = get_latest_baidu_messages()
    return render_template('messages.html', messages=messages)
@app_webUI.route('/get_url')
def get_url():
    return render_template('get_url.html', share_baidu_key=str(share_baidu_key))

 
if __name__ == '__main__':
    app_webUI = Flask(__name__)
    app_webUI.run(debug=True, port=12301)