import time
import sqlite3
from functions.standardtime import standard_time


def append_log_to_table(db_path, log_timestamp, log_self, log_type, log_content):
    """
    向SQLite数据库中的 'logs' 表追加日志条目。

    :param db_path: SQLite数据库文件的路径。
    :param log_timestamp: 日志条目的时间戳。
    :param log_self: 日志条目的自标识。
    :param log_type: 日志的类型。
    :param log_content: 日志的内容。
    """
    log_timestamp=str(log_timestamp)
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 准备插入语句
        query = '''INSERT INTO logs (timestamp, self, type, content)
                   VALUES (?, ?, ?, ?)'''

        # 插入数据
        cursor.execute(query, (log_timestamp, log_self, log_type, log_content))

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

def append_call_to_table(db_path, log_timestamp, fm, to, result):
    """
    向SQLite数据库中的 'calls' 表追加日志条目。
    """
    log_timestamp=str(log_timestamp)
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 准备插入语句
        query = '''INSERT INTO calls (timestamp, [from], [to], result)
                   VALUES (?, ?, ?, ?)'''
        # 插入数据
        cursor.execute(query, (log_timestamp, str(fm), str(to), result))

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

def get_messages_from_database(db_path, include):
    pass

def get_listlength_messages_from_database(db_path, include):
    pass
    
            
class db():
    def __init__(self, db_path,phonenum,timezone=0):
       self.db_path = db_path
       self.phonenum=phonenum
       self.timezone=timezone
       self.standard_time=standard_time(timezone)
       
    def log(self, log_type, log_str):
        print(f"【{log_type}】【{self.standard_time.get()}】{log_str}")
        append_log_to_table(db_path=self.db_path, log_timestamp=time.time(), log_self=self.phonenum, log_type=log_type, log_content=log_str)
    def message(self, fm, to, content):
        append_message_to_table(db_path=self.db_path, log_timestamp=time.time(), fm=fm, to=to, content=content)
    def call(self, fm, to, result):
        append_call_to_table(db_path=self.db_path, log_timestamp=time.time(), fm=fm, to=to, result=result)
    def read_message(self, include):
        pass
        