# Dummy BitgetRestClient to simulate SDK presence
class BitgetRestClient:
    def __init__(self, api_key, api_secret, passphrase, use_server_time, base_url):
        pass
    def mix_market_get_latest_price(self, symbol, product_type):
        return {'data': {'price': '30000'}}
    def mix_account_set_leverage(self, symbol, product_type, margin_mode, leverage):
        pass
    def mix_order_place_order(self, symbol, product_type, margin_mode, side, order_type, price, size):
        return {'data': 'Simulated Order'}