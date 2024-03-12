import sqlite3, re, json
from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta

if __name__ == '__main__':
    app_statistics = Flask(__name__)
else:
    app_statistics=Blueprint('app_statistics', __name__)
DATABASE = 'database/mydatabase.db'


def get_top_ten_data(mode):
    if mode=="sender":
        mode="from"
    elif mode=="receiver":
        mode="to"
    else:
        mode="from"
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # 查询频率前十的数据
    cursor.execute(f"SELECT \"{mode}\", COUNT(\"{mode}\") FROM messages GROUP BY \"{mode}\" ORDER BY COUNT(\"{mode}\") DESC LIMIT 10")
    top_ten_data = cursor.fetchall()

    connection.close()

    return top_ten_data

@app_statistics.route('/ui/statistics/<mode>')
def web_statistics(mode):
    if mode=="sender" or mode=="receiver":
        return render_template('statistics.html', mode=mode)
    else:
        return jsonify({"status":False,"detail":f"No such mode: {mode}, /ui/statistics/sender or /ui/statistics/receiver"})
    


@app_statistics.route('/statistics/messages/<mode>')
def api_statistics_messages(mode):
    if mode=="sender" or mode=="receiver":     
        top_ten_data = get_top_ten_data(mode=mode)

        labels = [data[0] for data in top_ten_data]
        counts = [data[1] for data in top_ten_data]

        data = {
            'labels': labels,
            'counts': counts
        }

        return jsonify(data)
    else:
        return jsonify({"status":False,"detail":f"No such mode: {mode}, /ui/statistics/sender or /ui/statistics/receiver"})
    



if __name__ == '__main__':
    app_statistics.run(debug=True, port=12300)