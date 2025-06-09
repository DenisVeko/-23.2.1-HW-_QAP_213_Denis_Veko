# -23.2.1-HW-_QAP_213_Denis_Veko
## Итоговый проект. Создание парсера данных.
#### Задача проекта: построить парсер, принимающий информацию о категории товаров интернет-магазина Sunlight, возвращающий информацию о товарах с наивысшим рейтингом, построенном на основании оценок пользователей интернет-магазина. 
#### Полученную с помощью парсера информацию можно учитывать при формировании рекомендаций пользователям, маркетинге, расчете юнит-экономики, формировании акционных предложений.
#### Реализованную функцию можно будет интегрировать в потенциальный класс, который будет решать множество задач парсинга интернет-магазина Sunlight.
#### Выводные данные представляются в файле форма Excel.

``` python
# установка библиотек: # pip install beautifulsoup4 lxml
                       # pip install pandas openpyxl
# импорт необходимых библиотек
import requests
from bs4 import BeautifulSoup
import pandas as pd

# функция отбора информации о категории товаров по критерию максимального рейтинга на основании оценок пользователей интернет-магазина
def max_rating(category):

    page_num = 1 # переменной присвоить значение первой страницы пагинатора
    data = [] # создать пустой список для записи необходимой информации

    while True: # создать бесконечный цикл, который будет осуществлять поиск необходимой инфорамации по всем страницам каталога
        url = f'https://sunlight.net/catalog/{category}/page-{page_num}/' # URL интернет-магазина Sunlight, переменные {category}, {page_num} указать в URL
        content = requests.get(url) # запрос и сохранение информации с сайта по ссылке, заданной переменной url, в переменной content
        soup = BeautifulSoup(content.text, 'lxml') # создать объект BeautifulSoup, которому будет передаваться ответ на запрос и указать, что для парсинга необходимо использовать lxml
        entries = soup.find_all('div', class_='cl-item js-cl-item') # получить все элементы  <div> с классом cl-item js-cl-item, содержащем информацию о каждом товаре каталога на странице

        for entry in entries: # получить необходимые данные классов и атрибуты из каждого элемента entries посредством цикла for
            data_id = entry.attrs['data-id']
            article = entry.attrs['data-analytics-article']
            product_name = entry.attrs['data-analytics-name']
            rating = entry.find('div', class_='cl-item-info-rating').text.strip()
            price = entry.attrs['data-analytics-base-price']
            price_discount = entry.attrs['data-analytics-price']

            if rating == '5.0': # критерий отбора необходимой информации

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

df.to_excel('product_max_rating_brooch.xlsx') # вывод и запись необходимой информации в файл Excel```
