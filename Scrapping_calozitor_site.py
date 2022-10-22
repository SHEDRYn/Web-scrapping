import csv
from random import randrange
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import re

"""Код запроса"""
# url = 'https://calorizator.ru/product'
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36 "
}
# req = requests.get(url, headers=headers)
# src = req.text
"""Вывод в отдельный html файл"""
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

"""Сохраняем код страницы в переменную"""
# with open("index.html", "r", encoding="utf-8") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
#
# all_products_href = []
# all_products_class = soup.find_all(class_="product")
# for item in all_products_class[:-1]:
#     all_products_href += item.find_all(class_=re.compile("prod"))
#
# all_categories_dict = {}
# for prod in all_products_href:
#     prod_name = prod.text
#     prod_href = "https://calorizator.ru/" + prod.find("a").get("href")
#
#     all_categories_dict[prod_name] = prod_href
"""Вывод словаря с ссылками на категория продуктов в отдельный файл json"""
# with open("all_categories_dict.json", "w", encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding="utf-8") as file:
    all_categories = json.load(file)


iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():

    rep = [',', ' ', ',', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    """СОБИРАЕМ ЗАГОЛОВКИ ТАБЛИЦЫ"""
    table_head = soup.find(class_="views-table").find("thead").find_all("a")
    # или можно так products_data = soup.select('.views-table thead tr')
    product = table_head[0].text
    protein = table_head[1].text.replace(", ", "_")
    fat = table_head[2].text.replace(", ", "_")
    carbohydrate = table_head[3].text.replace(", ", "_")
    kcal = table_head[4].text.replace(", ", "_")

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                protein,
                fat,
                carbohydrate,
                kcal
            )
        )

    """СОБИРАЕМ ДАННЫЕ ПРОДУКТОВ"""
    table_body = soup.select(".views-table tbody tr")

    product_info = []
    for tr in table_body:
        product_tds = tr.find_all("td")

        title = product_tds[1].text.strip()
        protein_in_prod = product_tds[2].text.strip()
        fat_in_prod = product_tds[3].text.strip()
        carbohydrate_in_prod = product_tds[4].text.strip()
        kcal_in_prod = product_tds[5].text.strip()

        product_info.append(
            {
                "Title": title,
                "Protein": protein_in_prod,
                "Fat": fat_in_prod,
                "Carbohydrate": carbohydrate_in_prod,
                "Calories": kcal_in_prod
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    protein_in_prod,
                    fat_in_prod,
                    carbohydrate_in_prod,
                    kcal_in_prod
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}. {category_name} записан ...")
    iteration_count -= 1
    if iteration_count == 0:
        print("Работа завершена, покеда!")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(randrange(2))
