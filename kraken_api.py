import time
import base64
import hashlib
import hmac
import json
import urllib.parse as urllib
import requests
import math
import pandas as pd
import utils

class KrakenAPI():
    def __init__(self, apiPath, apiPublicKey="", apiPrivateKey=""):
        self.session = requests.Session()
        self.apiPath = apiPath
        self.apiPublicKey = apiPublicKey
        self.apiPrivateKey = apiPrivateKey

    ##### public endpoints #####

    # returns all instruments with specifications
    def get_instruments(self):
        endpoint = "/derivatives/api/v3/instruments"
        return self.make_request("GET", endpoint)

    # returns market data for all instruments
    def get_tickers(self):
        endpoint = "/derivatives/api/v3/tickers"
        return self.make_request("GET", endpoint)

    # returns the entire order book of a futures
    def get_orderbook(self, symbol):
        endpoint = "/derivatives/api/v3/orderbook"
        postUrl = "symbol=%s" % symbol
        return self.make_request("GET", endpoint, postUrl=postUrl)

    # returns historical data for futures and indices
    def get_history(self, symbol, lastTime=""):
        endpoint = "/derivatives/api/v3/history"
        if lastTime != "":
            postUrl = "symbol=%s&lastTime=%s" % (symbol, lastTime)
        else:
            postUrl = "symbol=%s" % symbol
        return self.make_request("GET", endpoint, postUrl=postUrl)
    
    # returns most recent candle data for a given resolution, symbol and tick type
    def get_recent_candle(self, resolution, symbol, tick_type):
        endpoint = f"/api/charts/v1/{tick_type}/{symbol}/{resolution}"
        return self.make_request("GET", endpoint)
    
    # returns the most recent n number of candles for a given resolution, symbol and tick type

    def get_n_candles(self, n, resolution, symbol, tick_type):
        n+=1
        num = ''.join(filter(str.isdigit, resolution))
        interval = ''.join(filter(str.isalpha, resolution))

        end = math.trunc(time.time())


        if interval == "m":
            start = end - (n*int(num)*60)
            end -= int(num)*60
        elif interval == "h":
            start = end - (n*int(num)*3600)
            end -= int(num)*3600
        elif interval == "d":
            start = end - (n*int(num)*86400)
            end -= int(num)*86400
        elif interval == "w":
            start = end - (n*int(num)*604800)
            end -= int(num)*604800

        endpoint = f"/api/charts/v1/{tick_type}/{symbol}/{resolution}"
        postUrl = f"from={start}&to={end}"

        return self.make_request("GET", endpoint, postUrl=postUrl)
    


    ##### private endpoints #####

    # returns key account information
    # Deprecated because it returns info about the Futures margin account
    # Use get_accounts instead
    def get_account(self):
        endpoint = "/derivatives/api/v3/account"
        return self.make_request("GET", endpoint)

    # returns key account information
    def get_accounts(self):
        endpoint = "/derivatives/api/v3/accounts"
        return self.make_request("GET", endpoint)

    # places an order
    def send_order(self, orderType, symbol, side, size, limitPrice, stopPrice=None, clientOrderId=None):
        endpoint = "/derivatives/api/v3/sendorder"
        postBody = "orderType=%s&symbol=%s&side=%s&size=%s&limitPrice=%s" % (
            orderType, symbol, side, size, limitPrice)

        if orderType == "stp" and stopPrice is not None:
            postBody += "&stopPrice=%s" % stopPrice

        if clientOrderId is not None:
            postBody += "&cliOrdId=%s" % clientOrderId

        return self.make_request("POST", endpoint, postBody=postBody)

    # places an order
    def send_order_1(self, order):
        endpoint = "/derivatives/api/v3/sendorder"
        postBody = urllib.urlencode(order)
        return self.make_request("POST", endpoint, postBody=postBody)

    # edit an order
    def edit_order(self, edit):
        endpoint = "/derivatives/api/v3/editorder"
        postBody = urllib.urlencode(edit)
        return self.make_request("POST", endpoint, postBody=postBody)

    # cancels an order
    def cancel_order(self, order_id=None, cli_ord_id=None):
        endpoint = "/derivatives/api/v3/cancelorder"

        if order_id is None:
            postBody = "cliOrdId=%s" % cli_ord_id
        else:
            postBody = "order_id=%s" % order_id

        return self.make_request("POST", endpoint, postBody=postBody)

    # cancel all orders
    def cancel_all_orders(self, symbol=None):
        endpoint = "/derivatives/api/v3/cancelallorders"
        if symbol is not None:
            postbody = "symbol=%s" % symbol
        else:
            postbody = ""

        return self.make_request("POST", endpoint, postBody=postbody)

    # cancel all orders after
    def cancel_all_orders_after(self, timeoutInSeconds=60):
        endpoint = "/derivatives/api/v3/cancelallordersafter"
        postbody = "timeout=%s" % timeoutInSeconds

        return self.make_request("POST", endpoint, postBody=postbody)

    # places or cancels orders in bat§
    def send_batchorder(self, jsonElement):
        endpoint = "/derivatives/api/v3/batchorder"
        postBody = "json=%s" % jsonElement
        return self.make_request("POST", endpoint, postBody=postBody)

    # returns all open orders
    def get_openorders(self):
        endpoint = "/derivatives/api/v3/openorders"
        return self.make_request("GET", endpoint)

    # returns filled orders
    def get_fills(self, lastFillTime=""):
        endpoint = "/derivatives/api/v3/fills"
        if lastFillTime != "":
            postUrl = "lastFillTime=%s" % lastFillTime
        else:
            postUrl = ""
        return self.make_request("GET", endpoint, postUrl=postUrl)

    # returns all open positions
    def get_openpositions(self):
        endpoint = "/derivatives/api/v3/openpositions"
        return self.make_request("GET", endpoint)

    # sends an xbt withdrawal request
    def send_withdrawal(self, targetAddress, currency, amount):
        endpoint = "/derivatives/api/v3/withdrawal"
        postBody = "targetAddress=%s&currency=%s&amount=%s" % (
            targetAddress, currency, amount)
        return self.make_request("POST", endpoint, postBody=postBody)

    # returns xbt transfers
    def get_transfers(self, lastTransferTime=""):
        endpoint = "/derivatives/api/v3/transfers"
        if lastTransferTime != "":
            postUrl = "lastTransferTime=%s" % lastTransferTime
        else:
            postUrl = ""
        return self.make_request("GET", endpoint, postUrl=postUrl)

    # returns all notifications
    def get_notifications(self):
        endpoint = "/derivatives/api/v3/notifications"
        return self.make_request("GET", endpoint)

    # makes an internal transfer
    def transfer(self, fromAccount, toAccount, unit, amount):
        endpoint = "/derivatives/api/v3/transfer"
        postBody = "fromAccount=%s&toAccount=%s&unit=%s&amount=%s" % (
            fromAccount, toAccount, unit, amount)
        return self.make_request("POST", endpoint, postBody=postBody)

    # accountlog csv
    def get_accountlog(self):
        endpoint = "/api/history/v2/accountlogcsv"
        return self.make_request("GET", endpoint)

    def _get_partial_historical_elements(self, elementType, **params):
        endpoint = "/api/history/v2/%s" % elementType

        params = {k: v for k, v in params.items() if v is not None}
        postUrl = urllib.urlencode(params)

        return self.make_request_raw("GET", endpoint, postUrl)

    def _get_historical_elements(self, elementType, since=None, before=None, sort=None, limit=1000):
        elements = []

        continuationToken = None

        while True:
            res = self._get_partial_historical_elements(elementType, since = since, before = before, sort = sort, continuationToken = continuationToken)
            body = json.loads(res.read().decode('utf-8'))
            elements = elements + body['elements']

            if res.headers['is-truncated'] is None or res.headers['is-truncated'] == "false":
                continuationToken = None
                break
            else:
                continuationToken = res.headers['next-continuation-token']

            if len(elements) >= limit:
                elements = elements[:limit]
                break

        return elements

    def get_orders(self, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves orders of your account. With default parameters it gets the 1000 newest orders.

        :param since: Timestamp in milliseconds. Retrieves orders starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves orders before this time.
        :param sort: String "asc" or "desc". The sorting of orders.
        :param limit: Amount of orders to be retrieved.
        :return: List of orders
        """

        return self._get_historical_elements('orders', since, before, sort, limit)

    def get_executions(self, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves executions of your account. With default parameters it gets the 1000 newest executions.

        :param since: Timestamp in milliseconds. Retrieves executions starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """

        return self._get_historical_elements('executions', since, before, sort, limit)

    def get_market_price(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves prices of given symbol. With default parameters it gets the 1000 newest prices.

        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves prices starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves prices before this time.
        :param sort: String "asc" or "desc". The sorting of prices.
        :param limit: Amount of prices to be retrieved.
        :return: List of prices
        """

        return self._get_historical_elements('market/' + symbol + '/price', since, before, sort, limit)

    def get_market_orders(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves orders of given symbol. With default parameters it gets the 1000 newest orders.

        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves orders starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves orders before this time.
        :param sort: String "asc" or "desc". The sorting of orders.
        :param limit: Amount of orders to be retrieved.
        :return: List of orders
        """

        return self._get_historical_elements('market/' + symbol + '/orders', since, before, sort, limit)

    def get_market_executions(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves executions of given symbol. With default parameters it gets the 1000 newest executions.

        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves executions starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """

        return self._get_historical_elements('market/' + symbol + '/executions', since, before, sort, limit)

    # signs a message
    def sign_message(self, endpoint, postData):
        if endpoint.startswith('/derivatives'):
            endpoint = endpoint[len('/derivatives'):]

        # step 1: concatenate postData, nonce + endpoint
        message = postData + endpoint

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf8'))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secretDecoded = base64.b64decode(self.apiPrivateKey)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secretDecoded, hash_digest,
                               hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64encode(hmac_digest)

    # sends an HTTP request
    def make_request_raw(self, requestType, endpoint, postUrl="", postBody=""):
        # create authentication headers
        postData = postUrl + postBody

        signature = self.sign_message(endpoint, postData)
        authentHeaders = {
            "APIKey": self.apiPublicKey,
            "Authent": signature}

        # create request
        if postUrl != "":
            url = self.apiPath + endpoint + "?" + postUrl
        else:
            url = self.apiPath + endpoint

        if requestType == "GET":
            response = self.session.get(url, params=str.encode(postBody), headers=authentHeaders)
        # elif requestType == "POST":
            # Need to finalise this for POST

        return response.json()

    # sends an HTTP request and read response body
    def make_request(self, requestType, endpoint, postUrl="", postBody=""):
        return self.make_request_raw(requestType, endpoint, postUrl, postBody)
    
    
    #### Local analysis and data management ####

    def get_candles_df(self, data):
        ohlc = ['open', 'high', 'low', 'close']
        our_data = []

        for candle in data['candles']:
            new_dict = {}
            new_dict['time'] = candle['time']
            new_dict['volume'] = candle['volume']
            for price in ohlc:
                new_dict[price] = candle[price]
            our_data.append(new_dict)

        df = pd.DataFrame.from_dict(our_data)
        df['time'] = pd.to_datetime(df['time'], exact=False, unit='ms')

        return df
    
    def save_file(self, candles_df, symbol, interval):
        candles_df.to_pickle(f"his_data/{symbol}_{interval}.pkl")

    def create_data(self, n, resolution, symbol, tick_type):
        data = self.get_n_candles(n, resolution, symbol, tick_type)
        df = self.get_candles_df(data)
        print(f"{symbol} loaded {df.shape[0]} candles from {df.time.min()} to {df.time.max()}")
        self.save_file(df, symbol=symbol, interval=resolution)

    def get_instruments_df(self):
        instrument_data = []
        data = self.get_instruments()
        for i in data['instruments']:
            if i['symbol'][:2] == "PF":
                new_ob = dict(
                name = i['symbol'],
                type = i['type']
                )
                instrument_data.append(new_ob)
        df = pd.DataFrame.from_dict(instrument_data)
        return df
    
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())



if __name__ == "__main__":
    api = KrakenAPI(apiPath="https://futures.kraken.com", 
                    apiPublicKey="<PUBLIC KEY HERE>", 
                    apiPrivateKey="<PRIVATE KEY HERE")
    api.save_instruments()