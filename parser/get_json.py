import requests
import json


headers = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.wildberries.ru",
    "priority": "u=1, i",
    "referer": "https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%87%D0%B8%D0%BF%D1%81%D1%8B",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
    "x-captcha-id": "Catalog 1|1|1730382870|AA==|88e02ffa7a964212a001a9065dfb2586|fRjiJehxOFGOi3zGwP38pOKhjzIdwgbLdSY5H9m9AW6",
    "x-queryid": "qid13067514172495308520241017135433",
}

params = {
    "ab_testing": "false",
    "appType": "1",
    "curr": "rub",
    "dest": "-1257786",
    "query": "",
    "resultset": "catalog",
    "sort": "popular",
    "spp": "30",
    "suppressSpellcheck": "false",
}


def get_data() -> json:
    response = requests.get(
        "https://search.wb.ru/exactmatch/ru/common/v7/search",
        params=params,
        headers=headers,
    )
    data = response.json()
    for product in data["data"]["products"]:
        product["sizes"][0]["price"] = get_product_price_with_wb_wallet(product["sizes"][0]["price"])
        product["product_link"] = get_product_link(product["id"])
        product["product_image"] = get_product_image_link(product["id"])
    return data


def get_product_price_with_wb_wallet(product_prices: dict) -> dict:
    product_prices["price_with_wb_wallet"] = int(product_prices["total"] * 0.97)
    for price_name, price in product_prices.items():
        if price != 0:
            product_prices[price_name] = price // 100
    return product_prices


def get_product_link(product_id: int) -> str:
    return f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"


def get_product_image_link(product_id: int) -> str:
    short_id = product_id // 100000
    if 0 <= short_id <= 143:
        basket = "01"
    elif 144 <= short_id <= 287:
        basket = "02"
    elif 288 <= short_id <= 431:
        basket = "03"
    elif 432 <= short_id <= 719:
        basket = "04"
    elif 720 <= short_id <= 1007:
        basket = "05"
    elif 1008 <= short_id <= 1061:
        basket = "06"
    elif 1062 <= short_id <= 1115:
        basket = "07"
    elif 1116 <= short_id <= 1169:
        basket = "08"
    elif 1170 <= short_id <= 1313:
        basket = "09"
    elif 1314 <= short_id <= 1601:
        basket = "10"
    elif 1602 <= short_id <= 1655:
        basket = "11"
    elif 1656 <= short_id <= 1919:
        basket = "12"
    elif 1920 <= short_id <= 2045:
        basket = "13"
    elif 2046 <= short_id <= 2189:
        basket = "14"
    elif 2190 <= short_id <= 2405:
        basket = "15"
    elif 2405 <= short_id <= 2621:
        basket = "16"
    elif 2621 <= short_id <= 2837:
        basket = "17"
    elif 2837 <= short_id <= 3053:
        basket = "18"
    else:
        basket = "19"

    return f"https://basket-{basket}.wbbasket.ru/vol{short_id}/part{product_id // 1000}/{product_id}/images/big/1.webp"
