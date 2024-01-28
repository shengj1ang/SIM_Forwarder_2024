import serial
import serial.tools.list_ports
import time
def DebugSerial():
    print("mode: debug-serial")
    serialPort=input("Port: ")
    baudRate=115200         
    ser=serial.Serial(serialPort,baudRate,timeout=0.5) 
    print("参数设置：串口=%s ，波特率=%d, Use ## to send exit signal"%(serialPort,baudRate))#输出串口号和波特率
    while True:
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
            return True
            
        #except Exception as ex:    
        #     print(ex)
        #     pass
            
        except Exception as ex:
            print(f"Something else went wrong: {str(ex)}")
        
    ser.close()
    return True
    
def get_ch340_port_list():
    port_list = list(serial.tools.list_ports.comports())
    List_CH340=[]
    for i in port_list:
        #print(i)
        if "CH340" in str(i):
            List_CH340.append(i)

    for j in List_CH340:
        print(j)
    return(List_CH340)
    
    
def get_port_list():
    port_list = list(serial.tools.list_ports.comports())
    for i in port_list:
        print(i)
    return port_list