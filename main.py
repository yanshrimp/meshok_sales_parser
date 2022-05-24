import requests
from bs4 import BeautifulSoup

from fake_useragent import UserAgent

user_agent = UserAgent()
headers = {"User-Agent": user_agent.chrome}


def get_html(url):
    session = requests.Session()
    r = session.get(url=url, headers=headers)
    if r.ok:
        return r.text
    else:
        return f'Сервер выдает ошибку!!! - {r.status_code}'


def get_all_prices(html):
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr', valign="top")
    sum_of_sales = 0
    data_counter = 0
    no_data_counter = 0

    for row in rows:
        try:
            tds = row.find('div', {'class': "fBack fPos"}).find('span', {'class': 'comment_sell'}).text.split('.')[0]
            sum_of_sales += int(tds)
            data_counter += 1
        except:
            no_data_counter += 1
    avg_of_one_sell = int(sum_of_sales / data_counter)
    potential = avg_of_one_sell * no_data_counter
    return f'Общая сумма продаж за период без лотов со скрытыми данными: {sum_of_sales}\nКол-во продаж/отзывов с открытыми данными (учтены в общей сумме): {data_counter}\nКол-во продаж/отзывов с закрытыми данными (не учтены в общей сумме): {no_data_counter}\nСредняя сумма на продажу (общая сумма/кол-во лотов с открытыми данными): {avg_of_one_sell}\nПотенциальная выручка за лоты с закрытыми данными(кол-во объяв с закрытыми данными * среднюю сумму продажи из открытых данных):{potential}\nПотенциальная общая сумма за период (сумма для лотов с открытыми данными + вероятная сумма для лотов с закрытыми данными): {sum_of_sales + potential}'


def main():
    url = 'https://meshok.net/info/361789/all'
    working_html = get_html(url)
    print(get_all_prices(working_html))


if __name__ == '__main__':
    main()
