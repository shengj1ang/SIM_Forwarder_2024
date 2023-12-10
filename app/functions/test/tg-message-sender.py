# -*- coding: utf-8 -*-
# pip install python-telegram-bot --upgrade
#https://api.telegram.org/bot5390778129:AAHZUjhhPOrxcZOvvueNo1_hfWscr4_fFCo/getupdates
  
import telegram

 
bot = telegram.Bot(token='5390778129:AAHZUjhhPOrxcZOvvueNo1_hfWscr4_fFCo')

 
#收发数据
 
while 1:
    try:
         i_text=input("Message Here: ")
         bot.send_message(chat_id='-1001636319740', text=i_text)
    except KeyboardInterrupt:
         break
         
    #except Exception as ex:    
    #     print(ex)
    #     pass
         
    except:
          print("【Log】Something else went wrong")
          bot.send_message(chat_id='-1001636319740', text="【程序错误】发现有小小的错误，可能需要来调试一下")
 