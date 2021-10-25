# https://www.youtube.com/watch?v=497Fy7CIBOk

from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

driver_path = 'D:\chalermporn.k\Desktop\Dataanalyst\Youtube_web_scraping_bs4_selenium\chromedriver.exe'
# driver_path = str(Path('chromedriver').resolve())
browser = webdriver.Chrome(executable_path= driver_path)

def write_csv(ads):
    with open('results.csv', 'a', newline='\n') as f:
        fields = ['title', 'price', 'url']
        writer = csv.DictWriter(f,fieldnames=fields)
        for ad in ads:
            writer.writerow(ad)
            print(ad)


def get_html(url):
    browser.get(url)
    return browser.page_source


def scrape_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
        url = ''
    else:
        title = card.h2.text.strip()
        url = card.h2.a.get('href')
    try:
        price = card.find('span', class_ = 'a-price-whole').text.strip('.').strip()
    except:
        price = ''
    else:
        price = ''.join(price.split(','))
    
    data = {'title': title, 'url': url, 'price':price }
    return data


def main():
    ads_data =[]
    for i in range(1,5):
        url = f'https://www.amazon.com/s?k=canon+5d&page={i}&qid=1605412642&ref=sr_pg_2'
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div', {'data-asin': True, 'data-component-type':'s-search-result'})
        print('len card = ',len(cards))

        for card in cards:
            data = scrape_data(card)   
            ads_data.append(data)

    write_csv(ads_data)


if __name__ == '__main__':
    main()