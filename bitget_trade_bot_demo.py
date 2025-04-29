from flask import Flask, request, jsonify
from bitget.rest_client import BitgetRestClient

app = Flask(__name__)

# === CONFIGURATION ===
API_KEY = "TA_CLE_API_BITGET"
API_SECRET = "TA_CLE_SECRET"
PASSPHRASE = "TA_PHRASE_SECRET"
BASE_URL = "https://api.bitget.com"

client = BitgetRestClient(api_key=API_KEY, api_secret=API_SECRET, passphrase=PASSPHRASE, use_server_time=True, base_url=BASE_URL)

DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_MARGIN_MODE = "crossed"
DEFAULT_LEVERAGE = "10"

@app.route('/')
def index():
    return "LegendBot is running!"

@app.route('/trade', methods=['POST'])
def execute_trade():
    try:
        data = request.get_json()
        signal = data.get("signal")
        amount = float(data.get("amount"))
        symbol = data.get("symbol", DEFAULT_SYMBOL)

        ticker = client.mix_market_get_latest_price(symbol=symbol, product_type="umcbl")
        price = float(ticker['data']['price'])
        quantity = round(amount / price, 3)

        side = "open_long" if signal == "LONG" else "open_short"

        client.mix_account_set_leverage(symbol=symbol, product_type="umcbl", margin_mode=DEFAULT_MARGIN_MODE, leverage=DEFAULT_LEVERAGE)

        order = client.mix_order_place_order(
            symbol=symbol,
            product_type="umcbl",
            margin_mode=DEFAULT_MARGIN_MODE,
            side=side,
            order_type="market",
            price=None,
            size=quantity
        )

        return jsonify({"message": f"Order executed: {order['data']}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

