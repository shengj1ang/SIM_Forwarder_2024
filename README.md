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

Schedule 
1. Rewrite Config file formats. (Done in 2023-12-03) 
2. Add all old logs&messages&calls to database (Done in 2023-12-03)
3. backend(main.py) prototype: database features. (Done in 2023-12-03)
4. Remove import Phone, make it as local function. (Done in 2023-12-03) 
5. Further function of backend: APIs (/api/message/send and /api/phone/call done in 2023-12-03, tested in 2023-12-04) 
6. WebServer UI Design prototype. (Call And Send Page in 2023-12-08)
7. Debugging...Futher plans...


<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/0.png"></img><p>USB转GSM模块 四频GSM/GPRS SIM80OC</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/1.png"></img><p>Console控制台</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/2.png"></img><p>Database</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/3.png"></img><p>Database</p>
<img src="https://raw.githubusercontent.com/shengj1ang/SIM_Forwarder_2024/main/img/4.png"></img><p>Telegram</p>