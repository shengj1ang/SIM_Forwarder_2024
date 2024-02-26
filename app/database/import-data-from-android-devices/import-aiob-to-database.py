# Read AIOB file from Android devices.
# https://play.google.com/store/apps/details?id=com.loopvector.allinonebackup.smsbackup&hl=en&gl=US
# You do need to charge for this app. Export AIOB file and read it here first.
# The AIOB file is a XML file in fact.


# Change This !!!
receiver="008613688888888"
file_path="aiob/SMS-1708912680479.aiob"



import xml.etree.ElementTree as ET
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
            
            
            
            
def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def parse_aiob_file(file_content):
    try:
        root = ET.fromstring(file_content)

        # 提取Type
        backup_type = root.find('Type').text
        print(f"Backup Type: {backup_type}")

        # 提取每个Datum的信息
        for datum in root.findall('.//Datum'):
            datum_id = datum.find('ID').text
            body = datum.find('BODY').text
            sent_date = datum.find('SENT_DATE').text
            received_date = datum.find('RECEIVED_DATE').text
            address = datum.find('ADDRESS').text
            
            #print(f"\nDatum ID: {datum_id}")
            print(f"Body: {body}")
            print(f"Sent Date: {sent_date}")
            print(f"Received Date: {received_date}")
            print(f"from: {address}")
            print("\n")
            append_message_to_table(db_path="../mydatabase.db", log_timestamp=sent_date[:10], fm=address, to=receiver, content=body)
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")




            
            
# 用法示例
#file_path = 'path/to/your/file.aiob'
file_content = read_binary_file(file_path)

if file_content:
    parse_aiob_file(file_content)

