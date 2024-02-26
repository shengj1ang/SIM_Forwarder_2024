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

def append_message_to_table(db_path, log_timestamp, phonenum, fm, to, content):
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
    res=[]
    with open(filepath,"r") as f:
        tmp_filecontent=f.readlines()
    for i in tmp_filecontent:
        if "来自" not in i and "内容" not in i:
            res[-1]=res[-1]+"\n"+i.replace("\n","").replace("<br>","").strip()
        res.append(i.replace("<br>","").strip())
    return res
        

def message_parser(array):
    res=[]
    for i in array:
        time=i[:i.find("【")].strip()
        tmp_part=i[i.find("【")-1:]
        #type
        tp=tmp_part[tmp_part.find("【")+1:tmp_part.find("】")]
        tmp_part=i[i.find("】")+1:]
        if "来自" in tmp_part and "接收号码" in tmp_part:
            fr=tmp_part[tmp_part.find("来自：")+3:tmp_part.find("接收号码")].strip()
            to=tmp_part[tmp_part.find("接收号码：")+5:tmp_part.find("内容")].strip()
            content=tmp_part[tmp_part.find("内容：")+3:].strip()
        else:
            to=get_self_phonenum()
            fr=tmp_part[tmp_part.find("来自：")+3:tmp_part.find("内容")].strip()
            content=tmp_part[tmp_part.find("内容：")+3:].strip()
        time=time_parser(time)
        res.append([time,tp,fr,to,content])
    return res
  
def time_parser(string):
    # Possible Formats: 2022-11-10,17:37:12 (UTC+00:00) 
    #                   2023-05-07,04:37:07 (UTC+01:00 British Summer Time) 
    #                   23/11/25,02:27:59 (GMT Standard Time)
    #                   1701579362.5628831
    try:
        BritishSummerTime=False
        # Unix Timestamp
        if "/" in string:
            string=string.replace("/","-")
            string="20"+string
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
        print(f"解析时间时出错: {e}, {string}")
        return 0


'''
#testfile="C:/Users/Administrator/Desktop/Apps/SIM_Forwarder_2024/app/database/FromOldVersion/html/SMS_2022-05-14.html"
testfile="C:/Users/Administrator/Desktop/Apps/SIM_Forwarder_2024/app/database/FromOldVersion/html/SMS_2022-11-16.html"


html=init_reading(testfile)
print(html)
messages=message_parser(html)
print(messages)

'''
if len(sys.argv) < 2:
    print("Invaild argv")
    sys.exit()
target_files=get_files_in_directory_with_extension_full_path(sys.argv[1],"html")
for target_file in target_files:
    html=init_reading(target_file)
    #print(html)
    messages=message_parser(html)
    #print(messages)
    
    for message in messages:
        if message[1]=="SMS" and message[0]!=0:
            print(message)
            append_message_to_table(db_path="../mydatabase.db", log_timestamp=message[0], phonenum=get_self_phonenum(), fm=message[2], to=message[3], content=message[4])
