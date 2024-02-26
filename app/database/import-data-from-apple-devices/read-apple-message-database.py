# 0. Idea from: https://blog.csdn.net/xihu_white/article/details/123006557
# 1. By using iCloud to backup all iPhone messages to MacOS computer
# 2. Database Location: ~/Library/Messages/chat.db
# 3. Test with this .py file



import sqlite3
from datetime import datetime


def read_messages_from_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # 使用提供的查询语句
    query_usertime = """
       SELECT
  a.[text] AS 短信内容,
  datetime(substr(a.[date],1,9)+978307200,'unixepoch','localtime') AS 接收时间,
  d.chat_identifier AS 发件人,
  a.destination_caller_id AS 收件人
FROM message a
LEFT JOIN chat_message_join b ON a.rowid = b.message_id
LEFT JOIN chat d ON b.chat_id = d.rowid
ORDER BY 接收时间 DESC;


    """


    query_timestamp = """
      SELECT
  a.[text] AS 短信内容,
  strftime('%s', datetime(substr(a.[date], 1, 9) + 978307200, 'unixepoch', 'localtime')) AS 接收时间,
  d.chat_identifier AS 发件人,
  a.destination_caller_id AS 收件人
FROM message a
LEFT JOIN chat_message_join b ON a.rowid = b.message_id
LEFT JOIN chat d ON b.chat_id = d.rowid
ORDER BY 接收时间 DESC;


    """

    cursor.execute(query_timestamp)
    messages = cursor.fetchall()

    for message in messages:
        content, timestamp, sender, receiver = message
        if sender:
            sender=sender.replace("+","00")
        if receiver:
            receiver=receiver.replace("+","00")
        # 打印消息信息
        print(f"短信内容: {content}")
        print(f"接收时间: {timestamp}")
        print(f"发件人: {sender}")
        
        print(f"收件人: {receiver}")
        print("\n")

    connection.close()

if __name__ == "__main__":
    # 指定Messages数据库路径
    #database_path = "~/Library/Messages/chat.db"
    database_path = "chat.db"
    read_messages_from_database(database_path)
