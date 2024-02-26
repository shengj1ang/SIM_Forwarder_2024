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

@app_statistics.route('/ui/statistics/sender')
def web_statistics_sender():
    return render_template('statistics.html', mode="sender")

@app_statistics.route('/ui/statistics/receiver')
def web_statistics_receiver():
    return render_template('statistics.html', mode="receiver")


@app_statistics.route('/statistics/messages/sender')
def api_statistics_messages_sender():
    top_ten_data = get_top_ten_data(mode="sender")

    labels = [data[0] for data in top_ten_data]
    counts = [data[1] for data in top_ten_data]

    data = {
        'labels': labels,
        'counts': counts
    }

    return jsonify(data)

@app_statistics.route('/statistics/messages/receiver')
def api_statistics_messages_receiver():
    top_ten_data = get_top_ten_data(mode="receiver")

    labels = [data[0] for data in top_ten_data]
    counts = [data[1] for data in top_ten_data]

    data = {
        'labels': labels,
        'counts': counts
    }

    return jsonify(data)

if __name__ == '__main__':
    app_statistics.run(debug=True, port=12300)