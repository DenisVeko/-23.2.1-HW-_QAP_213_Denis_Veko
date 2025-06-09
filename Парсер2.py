import requests
from bs4 import BeautifulSoup
import pandas as pd

# функция отбора информации о товарах по критерию максимального рейтинга на основании оценок пользователей интернет-магазина
def max_rating(category):

    page_num = 1
    data = []

    while True:
        url = f'https://sunlight.net/catalog/{category}/page-{page_num}/' # интернет-магазин Sunlight
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'lxml')
        entries = soup.find_all('div', class_='cl-item js-cl-item')

        for entry in entries:
            data_id = entry.attrs['data-id']
            article = entry.attrs['data-analytics-article']
            product_name = entry.attrs['data-analytics-name']
            rating = entry.find('div', class_='cl-item-info-rating').text.strip()
            price = entry.attrs['data-analytics-base-price']
            price_discount = entry.attrs['data-analytics-price']

            if rating == '5.0': # критерий поиска необходимой информации

                # запись необходимой информации в словарь
                data.append({'data_id': data_id, 'article': article, 'product_name': product_name,'rating': rating, 'price': price, 'price_discount': price_discount})


        if len(entries) < 60: # признак остановки - последняя страница включительно
            break
        page_num += 1 # переход на следующую страницу каталога
    return data


# вставить необходимую категорию товаров
# rings - кольца, clock - часы, piercings - пирсинг, chains - цепи, zaponki - запонки, bracelets - браслеты, necklace
# necklace - колье, aksessuary-sunlight - аксессуары, pendants - подвески, brooch - броши
product_max_rating = max_rating('brooch')

df = pd.DataFrame(product_max_rating)

df.to_excel('product_max_rating_brooch.xlsx') # вывод и запись необходимой информации в файл Excel

