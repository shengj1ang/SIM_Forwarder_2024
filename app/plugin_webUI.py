from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta
#from flask_wtf import FlaskForm
#from wtforms import StringField, DateTimeField
#from wtforms.validators import DataRequired
import sqlite3
DATABASE = 'database/mydatabase.db'
if __name__ == '__main__':
    app_webUI = Flask(__name__)
else:
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


def get_all_messages():
    try:
        # 连接到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 查询所有的记录
        cursor.execute('SELECT * FROM messages ORDER BY ROWID DESC;')
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
    mode = request.args.get('mode')
    if mode=="all":
        messages = get_all_messages()
    else:
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
@app_webUI.route('/myphones')
def ui_index():
    return render_template('index.html')

@app_webUI.route('/guests')
def ui_index_guests():
    return render_template('index_guests.html')    
 


@app_webUI.route('/ui/messages/add', methods=['GET', 'POST'])
def add_message():
    form = None  # Initialize form as None for GET requests

    if request.method == 'POST':
        try:
            timestamp_str = request.form.get('timestamp')
            #timestamp = datetime.strptime(timestamp_str + "+00:00", '%Y-%m-%dT%H:%M:%S%z').timestamp()
            


            sender = request.form.get('sender')
            receiver = request.form.get('receiver')
            content = request.form.get('content')  # Add this line for content field
            if sender==None or sender=="" or receiver==None or receiver=="" or content==None or content=="" or timestamp_str==None or timestamp_str=="":
                return jsonify({'success': False, 'message': f'sender==None or sender=="" or receiver==None or receiver=="" or content==None or content=="" or timestamp_str==None or timestamp_str==""'}) 
            
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M').timestamp()
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (timestamp, `from`, `to`, content) VALUES (?, ?, ?, ?)",
                           (timestamp, sender, receiver, content))

            conn.commit()
            conn.close()

            return jsonify({'success': True, 'message': 'Message added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})

    return render_template('add_message.html', form=form)


@app_webUI.route('/ui/messages/rebuild_database', methods=['POST'])
def rebuild_database():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 创建临时表并按 timestamp 字段排序
        cursor.execute("CREATE TEMPORARY TABLE temp_messages AS SELECT * FROM messages ORDER BY timestamp ASC")

        # 清空原表
        cursor.execute("DELETE FROM messages")

        # 将临时表中的数据复制回原表
        cursor.execute("INSERT INTO messages SELECT * FROM temp_messages")

        # 删除临时表
        cursor.execute("DROP TABLE temp_messages")

        # 执行 VACUUM 来压缩数据库文件
        #cursor.execute("VACUUM")

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Database rebuilt successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})




if __name__ == '__main__':
    app_webUI.run(debug=True, port=12301)