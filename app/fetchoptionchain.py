import requests
import json
import datetime


def pretty_print(data):
    json_object = json.loads(data)

    json_formatted_str = json.dumps(json_object, indent=2)

    print(json_formatted_str)


def get_option_chain_tda(symbol, fromdt, todt):
    fromdate = fromdt.strftime("%Y-%m-%d")
    todate = todt.strftime("%Y-%m-%d")
    url = "https://api.tdameritrade.com/v1/marketdata/chains?apikey=CZ5AZHH0IC4IUSJEWB7UAAGM0ZXWYYLS&strikeCount=20"
    url_with_params = url + "&symbol="+symbol+"&fromDate="+fromdate+"&toDate="+todate
    data = {
        "title": "Testing product",
        "price": 16.5,
        "description": "lorem ipsum set",
    }
    headers = {"Content-Type": "application/json"}

    response = requests.get(url_with_params, headers=headers)
    pretty_print(response.text)


if __name__ == "__main__":
    get_option_chain_tda("CHWY", datetime.date.today(), datetime.date.today() + datetime.timedelta(days=365))
