DATABASE = 'database/mydatabase.db'
merchant={
"UNKOWN":"⚠未知的商家⚠️",
"KFC":"快餐🍱", 
"AZUMA":"快餐🍱", 
"Burger":"快餐🍱", 
"Go Loc":"商店🏬", 
"Abdul":"商店🏬",
"W M MO":"商店🏬Morrisons",
"GYOZA":"中餐🥟",
"PEACE":"中餐🥟和平花园",
"Peace":"中餐🥟和平花园",
"SumUP":"第三方支付",
"SumUp":"第三方支付",
"COSTCU":"商店🏬",
"MAX SP":"照相📷",
"TESCO":"商店🏬",
"WAITRO":"商店🏬",
"ASDA H":"商店🏬",
"Lycamo":"运营商📱",
"TRINIT":"健身房🏋️",
"LONDON":"伦敦Oyster, 地下铁及公共交通",
"TRAINP":"火车票/汽车票/飞机票",
"GOOGLE":"Google线上扣款",
"MCDONA":"快餐🍱",
"WWW.BL":"Bloomberg",
"Red Ch":"中餐🥟红辣椒🌶️",
"BOLT.E":"打车🚖",
"HUNGRY":"熊猫外卖🐼",
"Jimmy?":"餐饮🦐",
"SH UK":"餐饮🦐",
"ARCHIE":"餐饮🦐",
"BABYLO":"餐饮🦐",
"Zettle":"第三方支付,餐饮零售",
"Taste":"商店🏬恒昇行",
"STGCOA":"公共交通🚌Stagecoach",
"SQ *SN":"餐饮🦐",
"Hungry":"熊猫外卖🐼",
"Red Re":"中餐🥟",
"Vue Ci":"🎬电影院🎦",
"Google":"Google线上扣款",
"WRIGHT":"餐饮🦐",
"SWEET":"小店📦VictoriaCoachStation",
"HUMAN":"共享自行车🚴",
"PANOPO":"小店📦",
"NYA*Sh":"小店📦",
"MARKS*":"快餐🍱", 
"Fetton":"餐饮🦐",
"VISA A":"美国签证办理费用🇺🇸",
"LYCAMO":"运营商📱",
"THE MI":"小店📦",
"SQ *DO":"餐饮🦐",
"THE NA":"商店🏬",
"MAMA T":"餐饮🦐",
"AMZNMk":"亚马逊🛍️",
"SQ *TA":"餐饮🦐",
"NYA*Be":"小店📦或自动售货机",
"AMAZON":"亚马逊🛍️",
"AMZNMK":"亚马逊🛍️",
"BERYL*":"共享自行车🚴",
"BERYL":"共享自行车🚴",
"UOM ST":"学费🏫",
"MY MAN":"学费🏫",
"UOM PR":"学费🏫",
"UOM AC":"学费🏫",
"RAILCA":"Rail Card",
"SAFEST":"仓库safestore.co.uk",
"CLOUDF":"Cloudflare边缘加速节点",
"DVSA":"Driving Standards Agency",
"HOLLAN":"保健品hollandandbarrett.com",
"CHICKE":"快餐🍱",
"NETIM":"域名注册商netim.com",
"NAVARR":"餐饮🦐",
"CONNEC":"可能是小店📦或自动售货机",
"TEAM B":"可能是餐饮🦐",
"NAVARR":"餐饮🦐",
"SPAR P":"可能是小店📦或自动售货机",
"WASABI":"餐饮🦐wasabi.uk.com",
"ONE HO":"商店🏬",
"MOSSBA":"可能是小店📦或自动售货机",
"GRAND":"快餐🍱",
"One Pl":"餐饮🦐",
"GOVIN":"可能是小店📦或自动售货机",
"RED CH":"中餐🥟红辣椒🌶️",
"Dixy":"快餐🍱",
"LIDL G":"商店🏬lidl.co.uk",
"POUNDL":"商店🏬Poundland",
"One Pl":"餐饮🦐",
"ZTL*VN":"可能是商店🏬",
"SHORYU":"餐饮🦐",
"iZ *Un":"可能是小店📦或自动售货机",
"PP*785":"Paypal"



}

import sqlite3, re, json
from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta
from functions.standardtime import timestamp_to_datetime

if __name__ == '__main__':
    app_bank = Flask(__name__)
else:
    app_bank=Blueprint('app_bank', __name__)

def merchant_classification(merchant_name):
    if merchant_name=="":
        return merchant_name
    try:
        merchant_type=merchant[merchant_name]
        return(f"{merchant_name}({merchant_type})")
    except Exception:
        return merchant_name
    
def get_timestamp_range(year, month):
    try:
        year = int(year)
        month = int(month)

        if 1 <= month <= 12:
            start_date = datetime(year, month, 1)
            
            # 单独处理12月，避免创建下一年的月份为13
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
            
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())
            return start_timestamp, end_timestamp
        else:
            print("Error in plugin_bank.py=>get_timestamp_range, 月份必须在1到12之间")
            return False
    except ValueError as e:
        print(f"Error in plugin_bank.py=>get_timestamp_range, 无效的年份或月份输入: {e}")
        return False

class Bank():
    def __init__(self):
        self.DB=DATABASE
    def parseCreditCardTransactions(self, content, ts=""):
        try:
            card_number=content[content.find("信用卡")+3:content.find("于")]
            if "交易失败" in content or "预授权" in content :
                merchant="";amount=""
            elif "网银" in content:
                merchant="";amount=""
            elif "消费" in content:
                merchant=content[content.find("在")+1:content.find("消费")]
                amount=content[content.find("消费")+2:content.find("元")]
                direction=-1
            elif "撤销" in content:
                merchant=content[content.find("在")+1:content.find("撤销")]
                if merchant=="":
                    merchant="撤销支付"
                amount=content[content.find("撤销")+2:content.find("元")]
                direction=1
            elif "存入" in content:
                merchant=content[content.find("在")+1:content.find("存入")]
                amount=content[content.find("存入")+2:content.find("元")]
                direction=1
            elif "成功退货" in content:
                merchant=""
                amount=content[content.find("成功退货")+4:content.find("元")]
                direction=1
            else:
                merchant="";amount=""
            if merchant=="":
                merchant="UNKOWN"
            merchant=merchant_classification(merchant)
            if amount!="":
                unit=amount[:3]
                amount=direction*float(amount[3:].replace(",","").replace(" ",""))
                return{"status":True,"ts":ts, "card_number":card_number,"merchant":merchant,"amount":amount, "unit":unit}
            
            return{"status":False,"detail":content}
        except Exception as ex:
            #print(ex);
            return{"status":False,"detail":ex}
            
    def readBankMessagesFromDB(self):
        conn = sqlite3.connect(self.DB)
        cursor = conn.cursor()
        query = """
        SELECT timestamp, content
        FROM messages
        WHERE content LIKE '%您的信用卡%'
        """
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            res=[]
            for row in results:
                #print(f"Timestamp: {row[0]}, Content: {row[1]}")
                #print(row)
                #print(self.parseCreditCardTransactions(row[1],ts=row[0]))
                after_parse=self.parseCreditCardTransactions(row[1],ts=row[0])
                if after_parse["status"]==True:
                    res.append(after_parse)
                else:
                    #print(after_parse)
                    pass
        finally:
            conn.close()
            return res


@app_bank.route('/bank/chart/<year>')
def web_bank_chart(year):
    try:
        #year=request.args.get('year')
        final_unit = request.args.get('unit')
        
        if final_unit:
            final_unit=final_unit.upper()
        #return f"Received month value: {month}"
        labels = []
        data=[]
        if year:
            year=int(year)
        else:
            return jsonify({"status":False, "detail":"Year not given"})
        if 2000<=year<=9999:
            transactions=Bank().readBankMessagesFromDB()
            for m in range(1,13):
                #print(get_timestamp_range(year,m))
                from_date, to_date=get_timestamp_range(year,m)
                res=[]
                for u in transactions:
                    if from_date<=float(u["ts"])<=to_date:
                        res.append(u)
                res_sum=0
                for v in res:
                    if v["unit"]=="GBP":
                        unit=9
                    elif v["unit"]=="CNY":
                        unit=1
                    elif v["unit"]=="HKD":
                        unit=1,1
                    elif v["unit"]=="USD":
                        unit=7
                    elif v["unit"]=="EUR":
                        unit=8
                    else:
                        unit=1
                    res_sum+=float(v["amount"])*unit
                if final_unit=="CNY":
                    pass
                elif final_unit=="GBP":
                    res_sum=res_sum/9
                elif final_unit=="USD":
                    res_sum=res_sum/7
                else:
                    pass
                labels.append(f'{m}')
                data.append(res_sum)
            #return all
            if final_unit==None or final_unit=="":
                final_unit="CNY"
            return render_template('chart.html', labels=labels, data=data, final_unit="Amount in "+final_unit, year=year, unit=final_unit)
        else:
            return jsonify({"status":False, "detail":"Invalid year or month range: 2000<=year<=9999, 1<=month<=12, /sum/<year>/<month>?unit=USD"})
    except ValueError:
        return jsonify({"status":False, "detail":"Invalid month value. Please provide a valid integer for month."})


    # 准备数据给Chart.js
    #labels = sorted(monthly_sums.keys())  # 确保标签是排序的
    #data = [monthly_sums[month] for month in labels]

    # 渲染HTML模板
    #return render_template('chart.html', labels=json.dumps(labels), data=json.dumps(data))


@app_bank.route('/bank/list/<year>/<month>')
def web_bank_list(year, month):
    try:
        #month = request.args.get('month')
        #return f"Received month value: {month}"
        
        year=int(year); month=int(month)
        if 2000<=year<=9999 and 1<=month<=12:
            transactions=Bank().readBankMessagesFromDB()
            from_date, to_date=get_timestamp_range(year,month)
            res=[]
            for u in transactions:
                if from_date<=float(u["ts"])<=to_date:
                    res.append(u)
            return jsonify(res)
        else:
            return jsonify({"status":False, "detail":"Invalid year or month range: 2000<=year<=9999, 1<=month<=12, /sum/<year>/<month>"})
    except ValueError:
        return jsonify({"status":False, "detail":"Invalid month value. Please provide a valid integer for month."})


@app_bank.route('/bank/sum/<year>/<month>')
def web_sum(year, month):
    try:
        final_unit = request.args.get('unit')
        if final_unit:
            final_unit = final_unit.upper()

        year = int(year)
        month = int(month)

        if 2000 <= year <= 9999 and 1 <= month <= 12:
            transactions = Bank().readBankMessagesFromDB()
            from_date, to_date = get_timestamp_range(year, month)

            res = []
            for u in transactions:
                if from_date <= float(u["ts"]) <= to_date:
                    res.append(u)

            res_sum = 0
            for v in res:
                if v["unit"] == "GBP":
                    unit = 9
                elif v["unit"] == "CNY":
                    unit = 1
                elif v["unit"] == "HKD":
                    unit = 1.1
                elif v["unit"] == "USD":
                    unit = 7
                elif v["unit"] == "EUR":
                    unit = 8
                else:
                    unit = 1

                res_sum += float(v["amount"]) * unit

            response_data = {"status": True, "amount": res_sum}

            if final_unit == "CNY":
                response_data["unit"] = "CNY"
                return jsonify(response_data)
            elif final_unit == "GBP":
                response_data["unit"] = "GBP"
                response_data["amount"] /= 9
                return jsonify(response_data)
            elif final_unit == "USD":
                response_data["unit"] = "USD"
                response_data["amount"] /= 7
                return jsonify(response_data)
            else:
                response_data["unit"] = "CNY"
                response_data["info"] = "unit allowed: CNY, GBP, USD. CNY as default. /sum/<year>/<month>?unit=USD"
                return jsonify(response_data)

        else:
            return jsonify({"status": False, "detail": "Invalid year or month range: 2000<=year<=9999, 1<=month<=12, /sum/<year>/<month>?unit=USD"})

    except ValueError:
        return jsonify({"status": False, "detail": "Invalid month value. Please provide a valid integer for month."})

if __name__ == '__main__':
    app_bank.run(debug=True, port=12300)