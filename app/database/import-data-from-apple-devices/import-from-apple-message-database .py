# 0. Idea from: https://blog.csdn.net/xihu_white/article/details/123006557
# 1. By using iCloud to backup all iPhone messages to MacOS computer
# 2. Database Location: ~/Library/Messages/chat.db
# 3. Test with this .py file



import sqlite3
from datetime import datetime
import time



def append_message_to_table(db_path, log_timestamp, fm, to, content):
    """
    向SQLite数据库中的 'messages' 表追加日志条目。
    """
    log_timestamp=str(log_timestamp)
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 准备插入语句
        query = '''INSERT INTO messages (timestamp, [from], [to], content)
                   VALUES (?, ?, ?, ?)'''
        #print(query, (log_timestamp, str(fm), str(to), content))
        # 插入数据
        cursor.execute(query, (log_timestamp, str(fm), str(to), content))

        # 提交更改
        conn.commit()
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"查询异常: {e}")
    finally:
        # 关闭数据库连接
        if conn:
            conn.close()
            
            
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
        if float(timestamp)>float(1708911627):
            print("在指定日期之后，添加到数据库")
            #append_message_to_table(db_path="../mydatabase.db", log_timestamp=timestamp, fm=sender, to=receiver, content=content)
        else:
            print("没有在指定日期之后，跳过")
        print("\n")

    connection.close()

if __name__ == "__main__":
    # 指定Messages数据库路径
    #database_path = "~/Library/Messages/chat.db"
    database_path = "chat.db"
    read_messages_from_database(database_path)
