import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time





prefectures = ["tokyo"]

links = []
shop_names = [] 
genres = []
phones = []
addresses = []
operation_times = []
regular_holidays = []
down_budgets = []
up_budgets = []

for prefecture in prefectures:
    for i in range(0,60):
        time.sleep(2)
        page = i+1
        print("page",page)
        url = f"https://tabelog.com/{prefecture}/rstLst/{page}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        shop_links = soup.find_all("a", class_='list-rst__rst-name-target cpy-rst-name')
        for v in shop_links:
            shop_link = v.get("href")
            links.append(shop_link)






for shop_detail_link in links:
    time.sleep(2)
    print("shop_detail_link",shop_detail_link)
    res = requests.get(shop_detail_link)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table",class_="c-table c-table--form rstinfo-table__table")


    rows = table.find_all("tr")



    for i,row in enumerate(rows):
        td = row.find("td")
        if i == 0:
            try:
                shop_name = td.text
                shop_names.append(shop_name)
                print("shop_name",shop_name)
            except Exception as e:
                shop_names.append("")
        elif i == 1:
            try:

                genre = td.text
                genres.append(genre)
                print("genre",genre)
            except:
                genre = ""
                genres.append(genre)
        elif i == 2:
            try:
                phone = td.text
                phones.append(phone)
                print("phone",phone)
            except Exception as e:
                phones.append(phone)
                print("phone",phone)
        elif i == 4:
            try:

                preAddress = td.text
                address = preAddress.split("大きな地図を見る")[0]
                addresses.append(address)
                print("address",address)
            except Exception as e:
                addresses.append(phone)
                print("phone",phone)                
            
        elif i == 6:
            v = td.text
            pre = v.split("定休日")
            operation_time = pre[0].replace("営業時間","")
            operation_times.append(operation_time)
            try:
                regular_holidays.append(pre[1])
                print("operation_time",operation_time)
                print("regular_holiday",pre[1])
            except Exception as e:
                regular_holidays.append("")
        elif i == 7:
            try:
                budget = td.find("em",class_="gly-b-dinner").text
                v = budget.split("～")
                down_budget = v[0]
                up_budget = v[1]
                down_budgets.append(down_budget)
                up_budgets.append(up_budget)
                

            except Exception as e:
                print("e",e)
                down_budgets.append("")
                up_budgets.append("")


print("shop_names",len(shop_names))
print("genres",len(genres))
print("addresses",len(addresses))
print("phones",len(phones))
print("down_budgets",len(down_budgets))
print("up_budgets",len(up_budgets))
print("regular_holidays",len(regular_holidays))
print("operation_times",len(operation_times))
print("links",len(links))


    
df = pd.DataFrame({
    "店名":shop_names,
    "ジャンル":genres,
    "住所":addresses,
    "電話番号":phones,
    "予算目安(下代)":down_budgets,
    "予算目安(上代)":up_budgets,
    "定休日":regular_holidays,
    "営業時間":operation_times,
    "店のリンク":links,


})

df.to_csv('./shop_details.csv')

