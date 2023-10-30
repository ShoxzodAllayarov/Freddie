from io import BytesIO
import requests
from bs4 import BeautifulSoup
import config
from backend.models import Product, Category, Image, PriceAndTitle
from time import sleep

# Замените эту ссылку на URL вашего сайта

URL = 'https://rastarasha-seed.space/semena/FastBuds-Seeds/page-PAGE/'
a = '''

Cali Buds SC
Dahood Urban Seeds
Delicious Seeds
                    Doctors Choice
Dutch Bulk Seeds
Dutch Passion
FastBuds Seeds


Grass-O-Matic
Green House Seeds
IZI
Kalashnikov
Medical Seeds
Nirvana Seeds
Paradise
Pyramid Seeds
Rabank
Rastaman Seeds
Ripper Seeds
Royal Queen
SeedStockers
Serious Seeds
Speed Seeds
Strong Seeds
Super Sativa Seed Club
Sweet Seeds
Trikoma Seeds
UKHTA
World of Seeds
'''
# Отправка HTTP GET запроса к сайту
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        
        return response.text
    
    
    print(response.status_code)
def parse():
    parent = Category.objects.get(id=1)
    category, success = Category.objects.get_or_create(name='FastBuds Seeds', parent=parent)
    for page in range(1, 8):
        url = URL.replace('PAGE', str(page))
        print(url)
        page_content = get_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')
        urls = []
        for card in soup.find_all('div', class_='ty-product-list clearfix'):
            urls.append(card.find('a', class_='product-title')['href'])
        for card in soup.find_all('div', class_='ty-product-list clearfix pr_out_stock'):
            urls.append(card.find('a', class_='product-title')['href'])
        for card_url in urls:
            sleep(2)
            try:
                page_content = get_page_content(card_url)
                card_soup = BeautifulSoup(page_content, 'html.parser')
                description = card_soup.find('div', id='content_description').text
                title = card_soup.find('h1').text
                prices = []
                try:
                    prices = [(i.find('span', class_='vr_name').text.strip(), ''.join(filter(lambda x: x.isdigit() or x == '.', i.find('bdi').find('span').text.strip())).split('.')[0]) for i in card_soup.find('ul', class_='ty-product-options__elem').find_all('li') if 'disabled="disabled"' not in str(i)]
                except Exception as e:
                    print(e)
                image = card_soup.find('a', class_='cm-image-previewer').get('href')
                image_url = image

                response = requests.get(image_url)
                
                product = Product.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    link=card_url
                )
                new_image = Image.objects.create(product=product)
                image_name = f'{product.id}_image.jpg'

                # Wrap response.content in a BytesIO object
                image_content = BytesIO(response.content)

                # Save the image file to the 'image' field of the Image object
                new_image.image.save(image_name, image_content, save=True)
                for price in prices:
                    PriceAndTitle.objects.create(product=product, price=int(price[1]), price_title=f'Упаковка: {price[0]}')
                print(page, title, len(description), prices, card_url)
            except Exception as e:
                print('sadasd', e)
        
        
        

parse()