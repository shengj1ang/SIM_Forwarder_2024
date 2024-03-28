from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return ("API")

@app.route('/home', methods=['GET'])
def home():
    return render_template('add.html')

@app.route('/api/log.php', methods=['GET', 'POST'])
def api_log():
    if request.method == 'POST':
        time_selection = request.form.get('Time')
        customTime= request.form.get('customTime')
        money_in_out = request.form.get('moneyInOut')
        payment_method = request.form.get('paymentMethod')
        custom_payment_method = request.form.get('customPaymentMethod')
        # Add code to handle other form fields

        print(f"时间选择: {time_selection}")
        if time_selection == 'customTime':
            print(f"自定义时间: {customTime}")
        print(f"Money In/Out: {money_in_out}")
        print(f"支付方式: {payment_method}")
        if payment_method == 'customPayment':
            print(f"自定义支付方式: {custom_payment_method}")
        # Add code to handle other form fields
        return (f"时间选择: {time_selection}")
    else:
        return ("GET")
    

if __name__ == '__main__':
    app.run(debug=True,port=3000)

