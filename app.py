from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_trade_profit(buy_price, sell_price, ada_amount, fee_rate=0.0035):
    ada_after_buy_fee = ada_amount * (1 - fee_rate)
    ada_after_sell_fee = ada_after_buy_fee * (1 - fee_rate)
    total_buy_cost = buy_price * ada_amount
    total_sell_value = sell_price * ada_after_sell_fee
    net_profit = total_sell_value - total_buy_cost
    roi_percent = (net_profit / total_buy_cost) * 100
    return {
        "buy_cost": round(total_buy_cost, 2),
        "sell_value": round(total_sell_value, 2),
        "profit": round(net_profit, 2),
        "roi": round(roi_percent, 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        buy = float(data['buy_price'])
        sell = float(data['sell_price'])
        amount = float(data['ada_amount'])
        result = calculate_trade_profit(buy, sell, amount)
        return jsonify(result)
    except:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)
