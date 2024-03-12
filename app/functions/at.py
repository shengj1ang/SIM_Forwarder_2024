from .unicode import *
import time
import serial


def at_initialize(ser, db):
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

def call(ser, num):
    ser.write('atd{};'.format(str(num)).encode('utf-8') + b'\r\n')

defaultMyConfig={"sms_send_allow":True}
sms_queue=[] #发送短信的队列
# SMS_Queue 我还在想怎么写

def at_send_en_message(ser, target_number, text_content, MyConfig=defaultMyConfig):
    try:
        if defaultMyConfig["sms_send_allow"]==True:
            if inEnglish(text)==True:
                ser.write('AT+CMGF=1'.encode('utf-8') + b'\r\n')
                ser.write(f'AT+CMGS="{target_number}"'.encode('utf-8') + b'\r\n')
                ser.write(b'\r\n')
                time.sleep(0.1)
                ser.write(text.encode('utf-8') + b'\r\n')
                time.sleep(0.2)
                command_variable = chr(26)
                ser.write(command_variable.encode('utf-8'))
                return((True,""))
            else:
                 return((False,"消息不是纯英文消息"))
        else:
            return((False,"sms_send_allow=False，全局消息发生被禁用！"))
    except Exception as e:
        return(False,str(e))   
        
def at_send_cn_message(ser, target_number, text_content, MyConfig=defaultMyConfig):
    try:
        if MyConfig["sms_send_allow"]==True:
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
            return((True,""))
    
        else:
            return((False,"sms_send_allow=False，全局消息发生被禁用！"))
    except Exception as e:
        return(False,str(e))
