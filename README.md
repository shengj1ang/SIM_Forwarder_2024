# SIM_Forwarder_2024

**Base on SIM800_AT_Python**

* Reject calls/accept/forward/send text messages through SIM800 module and AT commands. Supports multiple input and output methods. 

* 通过SIM800模块和AT指令拒绝电话/接受/转发/发送短信。支持多种输入和输出方法。 

Changes in SIM_Forwarder_2024: 
1. Use Sqlite as database, instead of file system. 
2. TimeStamp will be saved as timestamp. 
3. 3 types of log: TERMINAL(pyserial), LOG_TG(Telegram), LOG(std_output) 
4. Remove virtual environment. Use more python native methods to implement functions and achieve the best compatibility. 

Database Desgin:

```
CREATE TABLE "calls" ( "timestamp" TEXT, "from" TEXT, "to" TEXT, "result" TEXT ); CREATE TABLE "messages" ( "timestamp" TEXT, "from" TEXT, "to" TEXT, "content" TEXT ); CREATE TABLE "logs" ( "timestamp" TEXT, "self" TEXT, "type" TEXT, "content" TEXT );
```

WebServer Design: 
API Desgin(Method: POST): Form Not in URL but like this Return json:

```
/api/message/send mode=[cn/en]&from=[]&to=[] 

    {"result":"suc/fail", "details":"xxx"} 

/api/phone/call from=[]&to=[] 

    {"result":"suc/fail", "details":"xxx"}

/api/message/read include_num=[]&index=[]&include_content=[]&share=[] /api/phone/read?include=

```
If the value of "from" in the posted form is "TEST", API will return test message.

Dev Details: Read app/Dev_Notes.txt

<h2>Hardware: SIM80OC</h2>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/0.png"></img><p>USB转GSM模块 四频GSM/GPRS SIM80OC</p>

<h2>webUI Demo (API also provided)</h2>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_messages.png"></img><p>Messages</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_Sendmessage.png"></img><p>Send a message</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_calls.png"></img><p>Call</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_call.png"></img><p>Make a call </p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_chart.png"></img><p>Plugin: Bank chart (Read bank messages from database)</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_baidu.png"></img><p>Share: Share to others. 共享网盘登录的动态验证码</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_addMessage.png"></img><p>Add messages to database manually. 手动添加消息到数据库</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/webUI/webUI_statistics.png"></img><p>Statistics</p>

<h2>Backend</h2>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/1.png"></img><p>Console控制台</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/2.png"></img><p>Database</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/3.png"></img><p>Database</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/4.png"></img><p>Database</p>

<h2>Telegram Push</h2>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/5.png"></img><p>Telegram</p>