'''
This importer.py is designed to import old version logs of SIM_Forwarder to SIM_Forwarder_2024 database.
 
'''

import sys,os
import dateutil.parser
import time
import re
import sqlite3

def get_self_phonenum():
    try:
        with open("phonenum.txt", "r") as f:
            return(f.readlines()[0].replace("\n",""))
    except Exception as e:
        print(e)
        return("")
        
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
            
            
def get_files_in_directory_with_extension(directory_path, extension):
    file_list = []
    for file in os.listdir(directory_path):
        if file.endswith(f".{extension}"):
            file_list.append(file)
    return file_list
    
def get_files_in_directory_with_extension_full_path(directory_path, extension):
    """
    这个函数返回给定目录中具有特定扩展名的文件的完整路径列表。
    
    :param directory_path: 存放文件的目录路径。
    :param extension: 要过滤的文件扩展名（例如 'txt'）。
    :return: 具有指定扩展名的完整文件路径列表。
    """
    file_list = []

    # 检查目录中的每个文件
    for file in os.listdir(directory_path):
        if file.endswith(f".{extension}"):
            # 追加完整的文件路径
            file_list.append(os.path.join(directory_path, file))

    return file_list
    
    
def init_reading(filepath):
    logcontent=[]
    with open(filepath,"r") as f:
        tmp_filecontent=f.readlines()
    for i in tmp_filecontent:
        if "【" not in i and "】" not in i or "内容" in i:
            logcontent[-1]=logcontent[-1]+"\n"+i.replace("\n","")
        else:
            logcontent.append(i.replace("\n",""))
    return logcontent

def log_parser(array):
    res=[]
    for i in array:
        log_type=i[:i.find("】")].replace("【","").replace("】","")
        tmp_part=i[i.find("】")+1:]
        log_time=tmp_part[:tmp_part.find("】")].replace("【","").replace("】","")
        log_content=tmp_part[tmp_part.find("】")+1:]
        log_time=time_parser(log_time)
        res.append([log_type,log_time,log_content])
    return res
        
def time_parser(string):
    # Possible Formats: 2022-11-10,17:37:12 (UTC+00:00) 
    #                   2023-05-07,04:37:07 (UTC+01:00 British Summer Time) 
    #                   23/11/25,02:27:59 (GMT Standard Time)
    #                   1701579362.5628831
    try:
        BritishSummerTime=False
        # Unix Timestamp
        if string.replace('.', '', 1).isdigit():
            return float(string)
        if "(" in string and ")" in string:
            
            if "British Summer Time" in string:
                BritishSummerTime=True
            string=string[:string.find("(")].replace(" ","")
        # 替换逗号为空格，以适应dateutil.parser
        string = string.replace(',', ' ')

        # 使用dateutil.parser解析时间字符串
        dt = dateutil.parser.parse(string)
        # 将解析的datetime对象转换为Unix时间戳
        ts = time.mktime(dt.timetuple())
        if BritishSummerTime==True:
            ts +=3600
        return ts
    except Exception as e:
        print(f"解析时间时出错: {e}")
        return 0



'''
#testfile="C:/Users/Administrator/Desktop/Apps/SIM_Forwarder_2024/app/log/LOG/LOG_2022-11-10.txt"
#testfile="C:/Users/Administrator/Desktop/Apps/SIM_Forwarder_2024/app/log/LOG/LOG_2023-11-29.txt"
testfile="C:/Users/Administrator/Desktop/Apps/SIM_Forwarder_2024/app/log/TG/LOG_TG_2022-11-24.txt"

logs=init_reading(testfile)
print(logs)
logs=log_parser(logs)
print(logs)

'''
phone_num=get_self_phonenum()
if len(sys.argv) < 2:
    print("Invaild argv")
    sys.exit()
target_files=get_files_in_directory_with_extension_full_path(sys.argv[1],"txt")
for target_file in target_files:
    logs=init_reading(target_file)
    logs=log_parser(logs)
    print(logs)
    for log in logs:
        append_log_to_table(db_path="../mydatabase.db", log_timestamp=log[1], log_self=phone_num, log_type=log[0], log_content=log[2])
