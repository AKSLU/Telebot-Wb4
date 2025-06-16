from main import *

def test_case_1():
    return bool_login(5959595) == False

def test_case_2():
    return bool_login(6685845705) == True

def test_get_product():
    art = "5007120"
    url = f"https://basket-01.wbbasket.ru/vol50/part5007/{art}/info/ru/card.json"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200 and "imt_name" in response.json()
  
print("test_case_1:", test_case_1())
print("test_case_2:", test_case_2())
print("test_get_product:", test_get_product())
