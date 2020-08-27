import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import NavigableString
import json
import csv

url = 'https://www.bigbasket.com/product/all-categories/'
myHeaders = {'user-agent': 'Chrome/56.0.2924.87'}
category_tree = []

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

for div in soup.find_all('div', attrs = {'class':'DropDownColum'}):
    category_node = {}
    category_node['category'] = div.find('span').text
    category_node['parent'] = ''
    category_tree.append(category_node)
    for li in div.find_all('li'):
        category_node = {}
        category_node['category'] = li.text
        category_node['parent'] = div.find('span').text
        category_tree.append(category_node)

# print(category_tree)
# for cat in category_tree:
#     print(cat)
url1 = "https://www.bigbasket.com/product/get-products/?slug="
url2 = []
url3 = "&page="
url4 = "&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc"
url2.append("fruits-vegetables")
url2.append("foodgrains-oil-masala")
url2.append("bakery-cakes-dairy")
url2.append("beverages")
url2.append("snacks-branded-foods")
url2.append("beauty-hygiene")
url2.append("cleaning-household")
url2.append("kitchen-garden-pets")
url2.append("eggs-meat-fish")
url2.append("gourmet-world-food")
url2.append("baby-care")
product_list = []
for cat in url2:
    for i in range (1,500):
        print(url1+cat+url3+str(i)+url4)
        html_text = json.loads(requests.get(url1+cat+url3+str(i)+url4, headers = myHeaders).content)
        try:
            for product in html_text['tab_info'][0]['product_info']['products']:
               product_details = {}
               product_details['Name']= product['llc_n']
               product_details['newFlag']= product['is_new']
               product_details['pack_desc']= product['pack_desc']
               product_details['desc']= product['p_desc']
               product_details['p_type']= product['p_type']
               product_details['category']= product['llc_s']
               product_details['sku']= product['sku']
               product_details['brand']= product['p_brand']
               product_details['sp']= product['sp']
               product_details['mrp']= product['mrp']
               product_details['Size']= product['w']
               product_details['Parent']= ''
               product_list.append(product_details)
               for product1 in product['all_prods']:
                   product_details = {}
                   product_details['Name']= product1['llc_n']
                   product_details['newFlag']= product1['is_new']
                   product_details['pack_desc']= product1['pack_desc']
                   product_details['desc']= product1['p_desc']
                   product_details['p_type']= product1['p_type']
                   product_details['category']= product1['llc_s']
                   product_details['sku']= product1['sku']
                   product_details['brand']= product1['p_brand']
                   product_details['sp']= product1['sp']
                   product_details['mrp']= product1['mrp']
                   product_details['Size']= product1['w']
                   product_details['Parent']= product['sku']
                   product_list.append(product_details)
        except KeyError:
            print("")

keys = product_list[0].keys()
with open('productlist_Updated.csv', 'w', encoding = "utf-8", newline = '') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(product_list)

# keys = category_tree[0].keys()
# print(keys)
# with open('category_tree_1.csv', 'w', encoding="utf-8", newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(category_tree)
    
