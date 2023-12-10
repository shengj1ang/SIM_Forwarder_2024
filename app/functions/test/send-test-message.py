# -*- coding: utf-8 -*-
#pip3 install pyserial
import serial
from idna import unicode 
import re
import ascii   

def decodeunicode(str):
    i=0
    res=""
    
    if len(str)%4==0:
         while i<len(str)/4:
             res=res+"\\u"+str[4*i:4*i+4].lower()
             i+=1
         res=res.encode('utf-8').decode('unicode_escape')
         return(res)
    else:
        return(str)
   

print("Program Starts")
 
#打开串口
 
serialPort="COM7"   #串口号
 
baudRate=115200       #波特率

msgreceived=1
ser=serial.Serial(serialPort,baudRate,timeout=0.5) 
 
print("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate))#输出串口号和波特率
 

 
#收发数据
 
while 1:
    try:
        #str = input("请输入要发送的数据（非中文）并同时接收数据: ")
        #ser.write((str+'\n').encode())
        res=ser.readline()
       
        #读取并解析短消息
        if res!=b'' and res!=b'\r\n' and res!=b'OK\r\n':
             print("【Terminal】"+str(res))#可以接收中文
             if b'+CMTI:' in res:
                 print("【INFO】有短信来了")
                 ser.write('AT+CMGL'.encode('utf-8') + b'\r\n')  #读取内存中所有短消息
             
                 #ser.write('AT+GMGD=1,4'.encode('utf-8') + b'\r\n')  #删除内存中所有短消息
             
             if b'+CMGL:' in res: #短消息第一部分-电话号码和时间
                 #print("【INFO】开始读取短信")
                 re_phonenum=re.compile(r'\d{5,}')
                 re_time=re.compile(r'\d{1,2}/\d{1,2}/\d{1,2},\d{1,2}:\d{1,2}:\d{1,2}')
                 msg_phonenum=re_phonenum.search(str(res))[0]
                 msg_time=re_time.search(str(res))[0]
                 msgreceived=0
                 continue
             if msgreceived==0: #短消息第二部分-文本内容
                 msg_content=decodeunicode(str(res)[2:-5])
                 msgreceived=1
                 #print("【INFO】读取短信完成")
                 print("【GUI】收到消息  "+"来自电话："+msg_phonenum+" 时间："+msg_time+" 内容："+msg_content)
                 msg=""
         
             # 拒绝所有电话
             if b'RING\r\n' in res:
                ser.write('AT+CLCC'.encode('utf-8') + b'\r\n') #获取来电号码
                ser.write('AT+CHUP'.encode('utf-8') + b'\r\n') #拒绝电话
                
             '''
             #向11位的手机号来电发送短信
             
             #不会发送CRTL+Z啊啊啊
         
         
             if b'CLCC' in res:
                re_phonenum=re.compile(r'\d{5,}')
                send_msg_phonenum=re_phonenum.search(str(res))[0]
                if len(send_msg_phonenum)==11:
                     print("【Log】向11位的手机号来电发送短信")
                     ser.write(b'AT+CMGF=1\r\n')
                     ser.write(b'AT+CMGS="'+bytes(send_msg_phonenum,'utf-8')+b'"\r\n')
                     ser.write(b'msg\r\n')
                     ser.write(ascii.ctrl('z'))
  '''         
    except KeyboardInterrupt:
         break
         
    #except Exception as ex:    
    #     print(ex)
    #     pass
         
    except:
          print("【Log】Something else went wrong")
    
ser.close() 
