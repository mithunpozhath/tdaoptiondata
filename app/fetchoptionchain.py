import requests
import json
import datetime

today = datetime.date.today()


def pretty_print(data):
    json_object = json.loads(data)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)


def get_option_chain_tda(symbol, fromdt, todt):
    fromdate = fromdt.strftime("%Y-%m-%d")
    todate = todt.strftime("%Y-%m-%d")
    url = "https://api.tdameritrade.com/v1/marketdata/chains?apikey=CZ5AZHH0IC4IUSJEWB7UAAGM0ZXWYYLS&strikeCount=1"
    url_with_params = url + "&symbol=" + symbol + "&fromDate=" + fromdate + "&toDate=" + todate
    headers = {"Content-Type": "application/json"}
    response = requests.get(url_with_params, headers=headers)
    # pretty_print(response.text)
    processed_data = init_process_option_chain_tda(response.json())
    return processed_data


def get_quote_tda(symbol):
    url = "https://api.tdameritrade.com/v1/marketdata/" + symbol + "/quotes?apikey=CZ5AZHH0IC4IUSJEWB7UAAGM0ZXWYYLS"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    # pretty_print(response.text)
    processed_data = process_quote_tda(response.json(), symbol)
    return processed_data


def init_process_option_chain_tda(_data):
    process_option_chain_tda(_data["callExpDateMap"])
    processed_data = process_option_chain_tda(_data["putExpDateMap"])
    return processed_data


def process_quote_tda(data, symbol):
    val = data[symbol]
    processed_data = {"stockclosePrice": val["closePrice"], "stockopenPrice": val["openPrice"],
                      "stockhighPrice": val["highPrice"],
                      "stocklowPrice": val["lowPrice"], "stock52WkHigh": val["52WkHigh"],
                      "stock52WkLow": val["52WkLow"],
                      "stockPercentChange": val["regularMarketPercentChangeInDouble"]}
    return processed_data


def process_option_chain_tda(data):
    List = []
    processed_data = {}
    for key in data.keys():
        optexpirydate = key.split(":")[0]
        for vals in data[key].values():
            for val in vals:
                symbol = val["symbol"].split("_")[0]
                opt_symbol = val["symbol"].split("_")[1]
                processed_data[opt_symbol] = {
                    "putCall": val["putCall"], "netChange": val["netChange"],
                    "percentChange": val["percentChange"], "volatility": val["volatility"],
                    "strikePrice": val["strikePrice"],
                    "daysToExpiration": val["daysToExpiration"], "bid": val["bid"],
                    "ask": val["ask"],
                    "mark": val["mark"], "delta": val["delta"], "gamma": val["gamma"],
                    "theta": val["theta"], "vega": val["vega"], "rho": val["rho"],
                    "openInterest": val["openInterest"], "multiplier": val["multiplier"],
                    "timeValue": val["timeValue"],
                    "lowPrice": val["lowPrice"],
                    "highPrice": val["highPrice"],
                    "theoreticalOptionValue": val["theoreticalOptionValue"],
                    "theoreticalVolatility": val["theoreticalVolatility"],
                    "intrinsicValue": val["intrinsicValue"],
                    "nonStandard": val["nonStandard"],
                    "inTheMoney": val["inTheMoney"]}
    return processed_data


if __name__ == "__main__":
    symbol = "CHWY"
    option_chain = get_option_chain_tda(symbol, datetime.date.today(),
                                        datetime.date.today() + datetime.timedelta(days=365))
    quote_data = get_quote_tda(symbol)
    today_date = today.strftime("%m%d%Y")
    print(today_date)
    # print(option_chain)
    # print(quote_data)
    full_data = {"id": symbol + today_date, "symbol": symbol, "datadate": today_date, "stockdata": quote_data,
                 "optiondata": option_chain}
    print(full_data)
