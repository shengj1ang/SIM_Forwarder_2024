# -*- coding: utf-8 -*-
#pip3 install pyserial
import serial
from idna import unicode 
import re
import ascii   
import signal
import time
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
        res=ser.readline()
        if res==b'':
             time.sleep(0.1)
             i_input=input("Command: ")
             if i_input=="##":
                 command_variable = chr(26)
                 ser.write(command_variable.encode('utf-8'))
             else:      
                 ser.write(i_input.encode('utf-8') + b'\r\n')
        else:
             print(res)
             i_input=input("Command: ")
             if i_input=="##":
                 command_variable = chr(26)
                 ser.write(command_variable.encode('utf-8'))
             else:      
                 ser.write(i_input.encode('utf-8') + b'\r\n')
       
    except KeyboardInterrupt:
         break
         
    #except Exception as ex:    
    #     print(ex)
    #     pass
         
    except:
          print("【Log】Something else went wrong")
    
ser.close() 
