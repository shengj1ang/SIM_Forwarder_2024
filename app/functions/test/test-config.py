import sys
import configparser

try:  
    if len(sys.argv)<=1:
        print("缺少参数，参数是配置文件（必填）")  
        sys.exit()
    cf=configparser.ConfigParser()
    cf.read(sys.argv[1])
    current_phonenum=cf.get('main','current_phonenum')
    max_error_count=cf.getint('main','max_error_count')

    serialPort=cf.get('port','serialPort')
    baudRate=cf.getint('port','baudRate')
    schedule_reconnect_max=cf.getfloat('port','schedule_reconnect_max')

    sms_send_allow=cf.getboolean('sms','sms_send_allow')
    sms_auto_send=cf.getboolean('sms','sms_auto_send')
    sms_limit=cf.getint('sms','sms_limit')
    sms_auto_send_content=cf.get('sms','sms_auto_send_content')

    current_phonenum_log=cf.getboolean('log','current_phonenum_log')

    tg_send_enable=cf.getboolean('telegram','tg_send_enable')
    tg_receive_enable=cf.getboolean('telegram','tg_receive_enable')
    #bot = telepot.Bot(cf.get('telegram','bot'))
    tg_chat_id=cf.get('telegram','tg_chat_id')
    current_phonenum_tg=cf.getboolean('telegram','current_phonenum_tg')
    tg_read_period=cf.getint('telegram','tg_read_period')
    common_input_function=cf.getboolean('common_input','common_input_function')
except:
    print('读取配置文件出错！')
    sys.exit()