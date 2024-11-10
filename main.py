import requests
from bs4 import BeautifulSoup

def login(session: requests.Session, url: str, data: dict) -> bool:
    """ログインを試み、成功すればTrueを返します。"""
    response = session.post(url, data=data)
    if LOGIN_SUCCESS_TEXT in response.text:
        print("ログイン成功")
        return True
    else:
        print("ログイン失敗")
        return False

def get_stock_data(session: requests.Session) -> tuple[bool, list]:
    """株の保有状況を取得し、保有している場合はデータを返します。
    第一返り値は保有しているかどうかの真偽値です。
    第二返り値は保有データの２次元リストです。銘柄コード、銘柄名、保有数、現在値、評価額の順番になってる。
    """
    response = session.get(STOCK_DATA_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='table_wrapper')
    
    if len(divs) < 2:
        print("2番目のdivが見つかりませんでした")
        return False, []
    
    second_div = divs[1]
    table = second_div.find('table', class_='Dealings sp_layout')
    rows = table.find_all('tr')[1:]  # ヘッダー行をスキップ
    
    data = [
        [col.text.strip().replace(',', '') for col in row.find_all('td')]
        for row in rows
    ]
    
    return bool(data), data

def send_order(session: requests.Session, url: str, data: dict) -> None:
    """注文を送信します。"""
    response = session.post(url, data=data)
    if response.status_code == 200:
        print("注文送信成功")
    else:
        print("注文送信失敗")

def get_total_assets(session: requests.Session) -> int | None:
    """資産合計を取得し、取得できない場合はNoneを返します。"""
    response = session.get('https://www.ssg.ne.jp/performances/team')
    soup = BeautifulSoup(response.text, 'html.parser')
    temo_stock_div = soup.find('div', id='temoStock')
    if temo_stock_div:
        table = temo_stock_div.find('table')
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                if len(rows) >= 2:
                    second_row = rows[1]
                    cols = second_row.find_all('td')
                    if cols:
                        total_assets = cols[0].text.strip().replace(',', '')
                        return int(total_assets)
    print("資産合計が見つかりませんでした")
    return None
