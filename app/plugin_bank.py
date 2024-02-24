import sqlite3, re, json
from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime, timedelta


app_bank=Blueprint('app_bank', __name__)

def timestamp_to_datetime(timestamp):
    try:
        timestamp=float(timestamp)
        # Using Python's datetime module to convert timestamp to a readable format
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error converting timestamp to datetime: {e}")
        return None
        
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
            print("月份必须在1到12之间")
            return False
    except ValueError as e:
        print(f"无效的年份或月份输入: {e}")
        return False

class Bank():
    def __init__(self):
        self.DB="database/mydatabase.db"
    def parseCreditCardTransactions(self, content, ts=""):
        try:
            card_number=content[content.find("信用卡")+3:content.find("于")]
            if "交易失败" in content or "预授权" in content :
                merchant="";amount=""
            elif "消费" in content:
                merchant=content[content.find("在")+1:content.find("消费")]
                amount=content[content.find("消费")+2:content.find("元")]
                direction=-1
            elif "撤销" in content:
                merchant=content[content.find("在")+1:content.find("撤销")]
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
                    print(after_parse)
        finally:
            conn.close()
            return res


@app_bank.route('/bank/chart/<year>')
def web_bank_chart(year):
    try:
        final_unit = request.args.get('unit')
        if final_unit:
            final_unit=final_unit.upper()
        #return f"Received month value: {month}"
        labels = []
        data=[]
        year=int(year)
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
    app_bank = Flask(__name__)
    app_bank.run(debug=True, port=12300)