# -*- coding: utf-8 -*-
import sys, time, re, threading, traceback
from flask import Flask, request, render_template, send_from_directory, redirect, jsonify
import serial
#import idna
from functions.config import UserConfig
from functions.telegram import tg_bot
from functions.unicode import *
from functions.phoneinfo import *
from functions.database import db
from functions.standardtime import standard_time
from plugin_bank import app_bank
from plugin_webUI import app_webUI
#内置常量
__version__="PROTOTYPE-2023-12-06-EDITION7"
en_uni=(" ","!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/","0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","[","\\","]","^","_","`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","{","|","}","~")
record_sms_phonenum=[] #存储已发送提示消息的手机号，避免重复发送，浪费话费。
msg_in_receiving=False #短信是否完全接收完毕
msg_in_sending=False #短信是否在发送
app = Flask(__name__)
flask_command=[""]
app.register_blueprint(app_bank, url_prefix='/')
app.register_blueprint(app_webUI, url_prefix='/')

def isnum(str):
    try:
        float(str)
        return True
    except Exception as e:
        return False

def trim_spaces_in_bytes(input_bytes):
    """
    Trims spaces from the beginning and end of each line in the given bytes object.

    :param input_bytes: A bytes object potentially with spaces at the start and end of its lines.
    :return: A new bytes object with spaces removed from the start and end of each line.
    """
    # Split the bytes into lines, trim each line, and then join them back into a single bytes object
    #return b'\n'.join(line.strip()+bytes(f"/*{random.randint(100000000,999999999)}*/","utf-8") for line in input_bytes.splitlines())
    return b'\n'.join(line.strip() for line in input_bytes.splitlines())
'''
@app.after_request
def remove_newlines(response):
    if response.content_type == 'text/html; charset=utf-8':
        response.set_data(trim_spaces_in_bytes(response.get_data()).replace(b'\n', b'').replace(b'\t', b''))
        return response
    else:
        return response
        
'''
      
@app.route('/')
def page_index():
    return "index"
    
@app.route('/ui/send')
@app.route('/ui/send_message')
@app.route('/ui/send-message')
def ui_send_message():
    global MyConfig
    return render_template('send_message.html', fm=MyConfig["phonenum"])

@app.route('/ui/call')
@app.route('/ui/phone_call')
def ui_phone_call():
    global MyConfig
    return render_template('phone_call.html', fm=MyConfig["phonenum"])

    
@app.route('/api/message/send', methods=['POST'])
def api_message_send():
    global flask_command
    if flask_command[0]!="":
        return jsonify({"result":"fail", "detail":"API Busy, Wait And Retry Later."})
    global MyConfig
    mode = request.form.get('mode')
    fm = request.form.get('from')
    to = request.form.get('to')
    content = request.form.get('content')
    if fm == "TEST":
        return jsonify({"result":"suc", "detail": "API Works"})
    if mode!="cn" and mode!="en":
        return jsonify({"result":"fail", "detail": f"Invalid Mode, Allowed Mode: cn, en. The mode you posted: {mode}"})
    if fm!=MyConfig["phonenum"]:
        return jsonify({"result":"fail", "detail": f"This requests api is not for phonenumber {fm}."})
    if isnum(to)==False:
        return jsonify({"result":"fail", "detail": "Invalid Target Phone Number."})
    if content.replace(" ","")=="":
        return jsonify({"result":"fail", "detail": "Empty Message is not acceptable. "})
    flask_command=["SEND",mode,to,content]
    return jsonify({"result":"suc", "detail": f"Command SEND MESSAGE from {fm} to {to} by mode-{mode} has been delivered, content: {content}, timestamp: {str(time.time())}"})

    
@app.route('/api/phone/call', methods=['POST'])
def api_phone_call():
    global flask_command
    if flask_command[0]!="":
        return jsonify({"result":"fail", "detail":"API Busy, Wait And Retry Later."})
    global MyConfig
    fm = request.form.get('from')
    to = request.form.get('to')
    if fm == "TEST":
        return jsonify({"result":"suc", "detail": "API Works"})
    if fm!=MyConfig["phonenum"]:
        return jsonify({"result":"fail", "detail": f"This requests api is not for phonenumber {fm}"})
    if isnum(to)==False:
        return jsonify({"result":"fail", "detail": "Invalid Target Phone Number"})
    flask_command=["CALL",to]
    return jsonify({"result":"suc", "detail": f"Command MAKE A CALL from {fm} to {to} has been delivered"})


    
def at_initialize():
    global ser
    db.log("LOG","AT_initializing...")
    ser.write('AT'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #No Response without this
    ser.write('ATE0'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline()))  #echo off
    ser.write('AT+CPIN?'.encode('utf-8') + b'\r\n') #SIM Card In?
    ser.write('AT+CLIP=1'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #显示来电号码，如果没有这条指令，则来电话模块只送出ring，不送出号码
    ser.write('AT+CMGF=1'.encode('utf-8') + b'\r\n')
    #ser.write('AT+CIMI'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #读取IMSI
    #ser.write('AT+CCID'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #读取ICCID号
    #ser.write('AT+CPBS="ON"'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #将电话存贮位置选择为本机号码列表
    #ser.write('AT+CPBW=1'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #储存本机号码
    #ser.write('AT+CNUM'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #读取本机号码
    #ser.write('AT+CSQ'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #检查网络信号强度和SIM卡情况命令返回：+CSQ: **,##
          #其中**应在10到31之间，数值越大表明信号质量越好，##应为99。
          #否则应检查天线或SIM卡是否正确安装
    #ser.write('AT+CGMR'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #查询模块版本
    #ser.write('AT+COPS=?'.encode('utf-8') + b'\r\n');time.sleep(1);db.log("TERMINAL",str(ser.readline())) #搜网
    
    return True

def at_send_en_message(phonenum,text):
    global ser
    global msg_in_sending
    global MyConfig
    try:
        if MyConfig["sms_send_allow"]==True:
            if msg_in_sending==False:
                for i in text or "\n"in text:
                    if i in en_uni:
                        pass
                    else:
                        return((False,"NOT_EN"))
                msg_in_sending=True
                ser.write('AT+CMGF=1'.encode('utf-8') + b'\r\n')
                ser.write('AT+CMGS="{}"'.format(phonenum).encode('utf-8') + b'\r\n')
                ser.write(b'\r\n')
                time.sleep(0.1)
                ser.write(text.encode('utf-8') + b'\r\n')
                time.sleep(0.2)
                command_variable = chr(26)
                ser.write(command_variable.encode('utf-8'))
                msg_in_sending=False
                db.message(fm=MyConfig["phonenum"], to=phonenum, content=text)
                db.log("SEND-EN",f"MESSAGE SENT TO {phonenum} FROM {MyCofnig['phonenum']}, Content:{text}")
                tg_send(f"【发送消息】从{MyCofnig['phonenum']} 到 {phonenum}, 内容:{text}")
                return((True,""))
            else:
                 return((False,"目前有消息在发送中"))
        else:
            return((False,"sms_send_allow=False，全局消息发生被禁用！"))
    except Exception as e:
        return(False,str(e))   
        
def at_send_cn_message(phonenum,text):
    global ser
    global msg_in_sending
    global MyConfig
    try:
        if MyConfig["sms_send_allow"]==True:
            if msg_in_sending==False:
                msg_in_sending=True
                ser.write('AT+CMGF=1'.encode('utf-8') + b'\r\n')
                time.sleep(0.1)
                ser.write('AT+CSCS="UCS2"'.encode('utf-8') + b'\r\n')
                time.sleep(0.1)
                ser.write('AT+CSMP=17,71,0,8'.encode('utf-8') + b'\r\n')
                time.sleep(0.1)
                ser.write('AT+CMGS="{}"'.format(EncodeUnicode(phonenum)).encode('utf-8') + b'\r\n')
                time.sleep(0.1)
                ser.write(EncodeUnicode(text).encode('utf-8') + b'\r\n')
                time.sleep(0.2)
                command_variable = chr(26)
                ser.write(command_variable.encode('utf-8'))
                msg_in_sending=False
                db.message(fm=MyConfig["phonenum"], to=phonenum, content=text)
                db.log("SEND-CN",f"MESSAGE SENT TO {phonenum} FROM {MyCofnig['phonenum']}, Content:{text}")
                tg_send(f"【发送消息】从{MyCofnig['phonenum']} 到 {phonenum}, 内容:{text}")
                return((True,""))
            else:
                 return((False,"目前有消息在发送中"))  
        else:
            return((False,"sms_send_allow=False，全局消息发生被禁用！"))
    except Exception as e:
        return(False,str(e))


def check_sms_limit(phonenum):
    if sms_limit==0:
        return((False,"Up To Limit"))
    else:
        if len(phonenum)==11:
            for i in record_sms_phonenum:
                if i[0]==phonenum and i[1]<sms_limit:
                    record_sms_phonenum[record_sms_phonenum.index(i)]=[phonenum,i[1]+1]
                    return((True,""))
                elif i[0]==phonenum and i[1]>=sms_limit:
                    return((False,"Up To Limit"))
            record_sms_phonenum.append([phonenum,1])
            return((True,""))
        else:
            return((False,"Phonenum Length Not 11"))

def phonenum_self(mode): #mode支持参数：enter输出末尾换行符，space末尾为空格。
    if MyConfig["phonenum"]=="" or MyConfig["current_phonenum_tg"]==False:
        return("")
    if mode=="enter":
        return(f"接收：{MyConfig['phonenum']}\n")
    elif mode=="space":
        return(f"接收：{MyConfig['phonenum']}")
    else:
         return("")

def call(num):
    global ser
    ser.write('atd{};'.format(str(num)).encode('utf-8') + b'\r\n')
    

def call10086():
    global ser
    db.log("CALL","Start To Call 10086")
    ser.write('atd10086;'.encode('utf-8') + b'\r\n')

def tg_send(msg):
    global MyConfig
    global tg
    if MyConfig["enable_telegram"]==False:
        db.log("LOG_TG","'enable_telegram' is set to False, so Telegram Bot will not start")
    else:
        tg.sendMessage(chat_id=MyConfig["tg_chat_id"], text=str(msg))

def is_running_in_cmd():
    return 'PROMPT' in os.environ or 'PYCHARM_HOSTED' in os.environ 
   
    
def loop():
    global ser, msg_in_receiving, msg_in_sending, record_sms_phonenum, tg, flask_command, MyConfig
    error_count=1 #初始错误次数值
    standard_time.get()
    db.log("LOG","Program Starts")
    db.log("LOG","参数设置：串口=%s ，波特率=%d"%(MyConfig["serialPort"],MyConfig["baudRate"])) #输出串口号和波特率
    at_initialize()
    while True:
        try:
            schedule_reconnect=time.time()
            res=ser.readline() #读取并解析短消息
            if res!=b'' and res!=b'\r\n':
                 db.log("TERMINAL",str(res))
                 if res==b'\x00':
                    db.log("LOG","检测到信号断连，重新连接串口")
                    ser.close()
                    time.sleep(3)
                    ser=serial.Serial(MyConfig["serialPort"],MyConfig["baudRate"],timeout=0.5) 
                    #at_initialize()
                    db.log("LOG","检测到信号断连，重新连接串口完成")
                 if b'+CMTI:' in res:
                     db.log("LOG","有短信来了")
                     ser.write('AT+CMGL'.encode('utf-8') + b'\r\n')  #读取内存中所有短消息
                 if b'+CMGL:' in res: #短消息第一部分-电话号码和时间
                     #开始读取短信
                     re_phonenum=re.compile(r'\d{5,}')
                     re_time=re.compile(r'\d{1,2}/\d{1,2}/\d{1,2},\d{1,2}:\d{1,2}:\d{1,2}')
                     if len(re_phonenum.search(str(res))[0])>24:
                         msg_phonenum=DecodeUnicode(re_phonenum.search(str(res))[0])
                     else:
                         msg_phonenum=re_phonenum.search(str(res))[0]
                     msg_time=re_time.search(str(res))[0]
                     msg_in_receiving=True
                     continue
                 if msg_in_receiving==True: #短消息第二部分-文本内容
                     msg_content=DecodeUnicode(str(res)[2:-5])
                     msg_in_receiving=False
                     #读取短信完成
                     #msg_phonenum=DecodeUnicode(msg_phonenum) #这里可能有gbk解码方面的问题，直接在第一步读取
                     phone_location=phoneinfo(msg_phonenum)
                     db.message(fm=msg_phonenum, to=MyConfig["phonenum"], content=msg_content)
                     if phone_location[0]=="Error":
                         db.log("LOG",f"【收到消息】来自：{msg_phonenum} {phonenum_self('space')}时间：{standard_time.get()} 内容：{msg_content}")
                         tg_send(f"【收到消息】\n来自：{msg_phonenum} \n{phonenum_self('enter')}时间：{standard_time.get()} \n内容：{msg_content}")
                     else:
                         db.log("LOG",f"来自：{msg_phonenum} ({phone_location[1]}) {phonenum_self('space')}时间：{standard_time.get()} 内容：{msg_content}")
                         tg_send(f"【收到消息】\n来自：{msg_phonenum} ({phone_location[1]}) \n{phonenum_self('enter')}时间：{standard_time.get()} \n内容：{msg_content}")
                     msg="" #删除内存中所有短消息
                     ser.write('AT+CMGD=1,2'.encode('utf-8') + b'\r\n')
                 # 拒绝所有电话
                 if b'RING\r\n' in res:
                    ser.write('AT+CLCC'.encode('utf-8') + b'\r\n') #获取来电号码
                    #time.sleep(1)
                    ser.write('AT+CHUP'.encode('utf-8') + b'\r\n') #拒绝电话
                 if b'CLCC' in res:
                    re_phonenum=re.compile(r'\d{5,}')
                    phonenum=re_phonenum.search(str(res))[0]
                    phone_location=phoneinfo(phonenum)
                    db.call(fm=phonenum, to=MyConfig["phonenum"], result="REFUSED")
                    if phone_location[0]=="Error":
                         db.log("LOG",f"【拒绝来电】 \n来自：{phonenum} {phonenum_self('space')}")
                         tg_send(f"【拒绝来电】 \n来自：{phonenum} {phonenum_self('space')}")
                    else:
                         db.log("LOG",f"【拒绝来电】 \n来自：{phonenum} ({phone_location[1]}) {phonenum_self('space')}")
                         tg_send("LOG",f"【拒绝来电】 \n来自：{phonenum} ({phone_location[1]}) {phonenum_self('space')}")
                 #向11位的手机号来电发送短信
                 if b'CLCC' in res:
                    re_phonenum=re.compile(r'\d{5,}')
                    send_msg_phonenum=re_phonenum.search(str(res))[0]
                    if MyConfig["sms_auto_send"]==True:
                        return_check_limit=check_sms_limit(send_msg_phonenum)
                        db.log("LOG",f"临时发短信次数记录：{str(record_sms_phonenum)}")
                        if return_check_limit[0]==True:
                            return_send_cn_message=at_send_cn_message(send_msg_phonenum,sms_auto_send_content)
                            if return_send_cn_message[0]==True:
                                db.log("LOG",f"发送自动回复短信， 号码：{send_msg_phonenum}")
                                db.message(fm=MyConfig["phonenum"], to=send_msg_phonenum, content=MyConfig["sms_auto_send_content"])
                            else:
                                db.log("LOG",f"发送自动回复短信失败， 原因{return_send_cn_message[1]}，号码：{send_msg_phonenum}")
                        elif return_check_limit[0]==False:
                            db.log("LOG",f"不发送自动回复短信，原因：{return_check_limit[1]}， 号码：{send_msg_phonenum}")
                    else:
                        db.log("LOG","自动发送短信回复来点功能为关闭状态")
                 schedule_reconnect=time.time()
            else:
                if time.time()-schedule_reconnect>MyConfig["schedule_reconnect_max"]:
                    ser.close()
                    time.sleep(1)
                    ser=serial.Serial(MyConfig["serialPort"],MyConfig["baudRate"],timeout=0.5) 
                    db.log("LOG","串口自动重连")
                    schedule_reconnect=time.time()
            #Flask Command
            if flask_command[0]!="":
                if flask_command[0]=="SEND":
                    if flask_command[1]=="cn":
                        at_send_cn_message(flask_command[2],flask_command[3])
                    elif flask_command[1]=="en":
                        at_send_en_message(flask_command[2],flask_command[3])
                    else:
                        pass
                elif flask_command[0]=="CALL":
                    if flask_command[1]=="10086":
                        call10086()
                    else:
                        call(flask_command[1])
                else:
                    pass
                flask_command[0]=""
            
        except KeyboardInterrupt:
             db.log("LOG","KeyboardInterrupt")
             break
        except Exception as ex:
              if "PermissionError" in str(ex) and "Access is denied" in str(ex):
                 db.log("LOG","错误信息：SerialException\n详细信息：错误导致程序退出。\n这个错误一般在初次配置的时候出现，一般性是串口配置错误，修改配置即可。\n但是在生产环境中，这是一个严重的错误，正常情况下是几乎不可能面临此错误。模块很有可能被异常移除，或者受到物理损坏，需要手动检查模块和串口连接状态后再启动。")
                 tg_send("【异常】SerialException\n详细信息：错误导致程序退出。\n这个错误一般在初次配置的时候出现，一般性是串口配置错误，修改配置即可。\n但是在生产环境中，这是一个严重的错误，正常情况下是几乎不可能面临此错误。模块很有可能被异常移除，或者受到物理损坏，需要手动检查模块和串口连接状态后再启动。")
                 break
              else:
                  db.log("LOG",f"【异常】{str(ex)}\n目前累计错误次数：{str(error_count)},错误次数上限：{str(MyConfig['max_error_count'])}")
                  tg_send(f"【异常】{str(ex)}\n目前累计错误次数：{str(error_count)},错误次数上限：{str(MyConfig['max_error_count'])}")
              traceback.print_exc()
              if error_count>=MyConfig["max_error_count"]:
                     db.log("LOG","【异常处理】Too Many Errors, auto exit")
                     break
              else:
                     error_count+=1 
    ser.close() 

if not is_running_in_cmd():
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw() 
    messagebox.showerror("SIM_Forward_2024", "🔔 Attention 提示\nYou should run this app in command line mode.\n请通过命令行运行此程序。")
    root.destroy()
    sys.exit(1)
    
argv=sys.argv
#print(argv)
if len(argv)<=1:
    print("Argument Required! Use 'help' to get help")
    flag_return=True
    sys.exit()


if argv[1]=='debug-serial':
    from functions.debug import DebugSerial
    DebugSerial()
elif argv[1]=='get-ch340-port-list':
    from functions.debug import get_ch340_port_list
    get_ch340_port_list()
elif argv[1]=='get-port-list':
    from functions.debug import get_port_list
    get_port_list()    
elif argv[1]=='phoneinfo':
    print(phoneinfo(input("PhoneNum: ")))
elif argv[1]=='telegram':
    if len(argv)<3:
        print("Miss an argument [config-file-path] \nUse 'help' to get help")
    else:
        MyConfig=UserConfig().read(argv[2])
        UserConfig().show(argv[2])
        standard_time=standard_time(MyConfig["timezone"])
        db=db(db_path=MyConfig["db_path"], phonenum=MyConfig["phonenum"], timezone=MyConfig["timezone"])
        tg=tg_bot(tg_api_base_link=MyConfig["tg_api_base_link"],bot_id=MyConfig["bot"])
        while 1:
            tg_send(input("Send To Telegram: "))
        
elif argv[1]=='run':
    if len(argv)<3:
        print("Miss an argument [config-file-path] \nUse 'help' to get help")
    else:
        MyConfig=UserConfig().read(argv[2])
        print(MyConfig)
        standard_time=standard_time(MyConfig["timezone"])
        ser=serial.Serial(MyConfig["serialPort"],MyConfig["baudRate"],timeout=0.5) 
        db=db(db_path=MyConfig["db_path"], phonenum=MyConfig["phonenum"], timezone=MyConfig["timezone"])
        tg=tg_bot(tg_api_base_link=MyConfig["tg_api_base_link"],bot_id=MyConfig["bot"])
        if MyConfig["flask_production_mode"]==False:
            flask_thread = threading.Thread(target=lambda: app.run(host=MyConfig["flask_host"],port=MyConfig["flask_port"],use_reloader=False))
        else:
            from waitress import serve
            flask_thread = threading.Thread(target=lambda: serve(app, host=MyConfig["flask_host"], port=MyConfig["flask_port"]))
        flask_thread.start()
        loop()
elif argv[1]=="help":
    if getattr(sys, 'frozen', False):
        #Running as exe
        help_main="main.exe"
    else:
        help_main="python main.py"
    print(f"""
    --- SIM_Forwarder_2024 HELP ---
    version: {__version__}
    {help_main} run [config-file-path]
    {help_main} debug-serial
    {help_main} get-ch340-port-list
    {help_main} get-port-list
    {help_main} phoneinfo
    {help_main} telegram [config-file-path]
    {help_main} help
    """)
else:
    print("Invalid Argument! Use 'help' to get help")