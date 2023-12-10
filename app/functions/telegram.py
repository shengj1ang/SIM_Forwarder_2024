import requests
import time
from functions.standardtime import standard_time


def advanced_requests(url):
    error=0
    while True:
        if error>5:
            return(False,"Too Many Errors")
        try:
            r=requests.get(url,timeout=5)
            return (True,r.content.decode("utf-8"))
        except Exception as ex:
            error+=1
            #print(ex)
            print("LOG_TG","【Error】{}".format(str(ex)))
            time.sleep(5)

     
            
class tg_bot():
    def __init__(self, tg_api_base_link="https://api.telegram.org",bot_id=""):
        self.tg_api_base_link = tg_api_base_link
        self.bot_id=bot_id
        
        
    def getMe(self):
        return (advanced_requests("{}/bot{}/getMe".format(self.tg_api_base_link,self.bot_id)))
    def getUpdates(self):
        return (advanced_requests("{}/bot{}/getUpdates".format(self.tg_api_base_link,self.bot_id)))
    def sendMessage(self,chat_id,text):
        return (advanced_requests("{}/bot{}/sendMessage?chat_id={}&text={}".format(self.tg_api_base_link,self.bot_id,chat_id,text)))
    def sendImage(self,chat_id,fileaddr,text=""):
        try:
            img = open(fileaddr, 'rb')
        except Exception as ex:
            return(False,str(ex))
        
        if text=="":
            url=f"{self.tg_api_base_link}/bot{self.bot_id}/sendphoto?chat_id={chat_id}"
        else:
            url=f"{self.tg_api_base_link}/bot{self.bot_id}/sendphoto?chat_id={chat_id}&caption={text}"
        error=0
        while True:
            if error>10:
                return(False,"Too Many Errors")
            try:
                r=requests.post(url, files={'photo': img},timeout=10)
                return (True,r.content.decode("utf-8"))
            except Exception as ex:
                error+=1
                #print(ex)
                print("LOG_TG","【Error】{}".format(str(ex)))
                time.sleep(5)           
        
        
#bot=tg_bot("https://api.telegram.org","1111111111:xxxxxxxxxxxxxxxxxx_xxxxxxxxxxxxxxx")
#print(bot.getUpdates())
#print(bot.sendMessage("000000000000","TEST"))