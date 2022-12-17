import requests

def update_signs_db():
    getter = requests.request(method="GET", url="https://www.binance.com/gateway-api/v1/public/asset/asset/get-all-asset").json()
    signs = []
    for coin in getter['data']:
        signs.append(coin['assetCode'])
    if len(signs) > 0:
        signs_db = open("signs_db.py", "r+")
        signs_db.seek(0)
        signs_db.truncate()
        signs_db.writelines(["SIGNS = [\n"])
        signs_db.writelines("\t\"" + coin + "\",\n" for coin in signs)
        signs_db.write("]")
        signs_db.close()
    else:
        print("Что-то пошло не так.")

if __name__ == "__main__":
    update_signs_db()