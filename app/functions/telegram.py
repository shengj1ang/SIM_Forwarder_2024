import requests
import time
import threading

def advanced_requests(url):
    error = 0
    while True:
        if error > 5:
            return (False, "Too Many Errors")
        try:
            r = requests.get(url, timeout=5)
            return (True, r.content.decode("utf-8"))
        except Exception as ex:
            error += 1
            print("LOG_TG", "【Error】{}".format(str(ex)))
            time.sleep(5)

class tg_bot():
    def __init__(self, tg_api_base_link="https://api.telegram.org", bot_id=""):
        self.tg_api_base_link = tg_api_base_link
        self.bot_id = bot_id

    def getMe(self):
        return advanced_requests("{}/bot{}/getMe".format(self.tg_api_base_link, self.bot_id))

    def getUpdates(self):
        return advanced_requests("{}/bot{}/getUpdates".format(self.tg_api_base_link, self.bot_id))

    def sendMessage(self, chat_id, text):
        def send_async():
            result = advanced_requests("{}/bot{}/sendMessage?chat_id={}&text={}".format(self.tg_api_base_link, self.bot_id, chat_id, text))
            #print("sendMessage result:", result)
        threading.Thread(target=send_async).start()

    def sendImage(self, chat_id, fileaddr, text=""):
        def send_image_async():
            try:
                img = open(fileaddr, 'rb')
            except Exception as ex:
                print(f"sendImage error: {str(ex)}")
                return 

            if text == "":
                url = f"{self.tg_api_base_link}/bot{self.bot_id}/sendphoto?chat_id={chat_id}"
            else:
                url = f"{self.tg_api_base_link}/bot{self.bot_id}/sendphoto?chat_id={chat_id}&caption={text}"
            error = 0
            while True:
                if error > 10:
                    print("sendImage error: Too Many Errors")
                    return
                try:
                    r = requests.post(url, files={'photo': img}, timeout=10)
                    #print("sendImage result:", r.content.decode("utf-8"))
                    return
                except Exception as ex:
                    error += 1
                    print("LOG_TG", "【Error】{}".format(str(ex)))
                    time.sleep(5)

        threading.Thread(target=send_image_async).start()

        
#bot=tg_bot("https://api.telegram.org","1111111111:xxxxxxxxxxxxxxxxxx_xxxxxxxxxxxxxxx")
#print(bot.getUpdates())
#print(bot.sendMessage("000000000000","TEST"))