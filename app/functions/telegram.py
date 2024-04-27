import requests
import time
import threading
import queue

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
        self.message_queue = queue.Queue()
        self.message_thread = threading.Thread(target=self.process_queue)
        self.message_thread.daemon = True
        self.message_thread.start()

    def getMe(self):
        return advanced_requests("{}/bot{}/getMe".format(self.tg_api_base_link, self.bot_id))

    def getUpdates(self):
        return advanced_requests("{}/bot{}/getUpdates".format(self.tg_api_base_link, self.bot_id))

    def process_queue(self):
        while True:
            item = self.message_queue.get()
            if item is None:
                break  # Allows the thread to exit
            chat_id, text = item
            self.sendMessage(chat_id, text)
            self.message_queue.task_done()

    def sendMessage(self, chat_id, text): #sendMessageImmediately
        url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(self.tg_api_base_link, self.bot_id, chat_id, text)
        result = advanced_requests(url)
        # print("sendMessage result:", result)
    
    def send_queued_message(self, chat_id, text):
        self.message_queue.put((chat_id, text))
    
    def sendMessageQueue(self, chat_id, text): #sendMessage in a queue
        threading.Thread(target=lambda: self.send_queued_message(chat_id, text)).start()
    

    def sendMessageDelay(self, chat_id, text, delay=1):
        def send_async():
            try:
                delay=float(delay)
            except Exception:
                delay=1
            time.sleep(delay)
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