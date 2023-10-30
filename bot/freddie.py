import telebot
from telebot import types
import time
import pytz
from threading import Thread
import schedule
import config
from datetime import datetime
from time import sleep
from django.core.files.base import ContentFile
import requests
from django.utils.text import slugify
from backend.models import BotUser, Template, Category, Product, Template2Button, Image, PriceAndTitle, ShopCard, Mailing, Purchase, Category1
import mimetypes, os

TOKEN = config.TOKEN
PURCHASES_ID = dict()
BACK = dict()
bot = telebot.TeleBot(TOKEN, parse_mode='html')

tz = pytz.timezone('UTC')
STATES = dict()
STATES_2 = dict()
MESSAGES2DELETE = dict()
def schedule_checker():
    check_payment = Purchase.objects.filter(status='Оплачен', schedule=False)
    for p in check_payment:
        p.schedule=True
        p.save()
        text = Template.objects.get(title='AC').text
        bot.send_message(p.user.chat_id, text)
    check_payment = Purchase.objects.filter(status='Отклонен', schedule=False)
    for p in check_payment:
        p.schedule=True
        p.save()
        text = Template.objects.get(title='DANIED').text
        bot.send_message(p.user.chat_id, text)

    mailings = Mailing.objects.filter(sent=False)
    for mailing in mailings:
        date = mailing.datetime
        date1 = tz.localize(datetime(date.year, date.month, date.day, date.hour, date.minute, date.second))
        date2 = datetime.now(tz)
        difference_in_seconds = (date1 - date2).total_seconds()
        if difference_in_seconds < 0 and difference_in_seconds > -300:
            mailing.sent = True
            mailing.save()
            for user in mailing.get_users():
                try:
                    text = mailing.message_text_ru
                    status_text = True
                    user_id = user.chat_id
                    mailing_loads = mailing.loads.all()
                    if not mailing_loads.exists():
                        bot.send_message(user_id, text, disable_web_page_preview=True)
                    for i in mailing_loads:
                        
                        if not status_text:
                            text = None
                        if i.type_choice == 'photo':
                            bot.send_photo(user_id, photo=open(i.file.path.replace('bot', 'app'), 'rb'), caption=text)
                        elif i.type_choice == 'video':
                            bot.send_video(user_id, video=open(i.file.path.replace('bot', 'app'), 'rb'), caption=text)
                        elif i.type_choice == 'document':
                            bot.send_document(user_id, open(i.file.path.replace('bot', 'app'), 'rb'), caption=text)
                        else:
                            bot.send_audio(user_id, audio=open(i.file.path.replace('bot', 'app'), 'rb'), caption=text)
                        if status_text:
                            status_text = False
                        sleep(0.1)
                except Exception as e:
                    print('err in mailing > ', e)
    


def delete_all_messages(chat_id):
    if chat_id in MESSAGES2DELETE.keys():
        for id in MESSAGES2DELETE[chat_id]:
            try:
                bot.delete_message(chat_id, id)
            except Exception:
                pass
        MESSAGES2DELETE[chat_id] = []

@bot.callback_query_handler(func=lambda call: True)
def callback_data_message(call):
    global STATES, MESSAGES2DELETE, PURCHASES_ID, BACK
    message = call.message
    chat_id = call.message.chat.id
    if chat_id not in MESSAGES2DELETE.keys():
        MESSAGES2DELETE[chat_id] = []
    data = call.data
    user = BotUser.objects.get(chat_id=chat_id)
    if chat_id not in BACK.keys():
       BACK[chat_id] = [data, data]
    else: 
        BACK[chat_id] = [BACK[chat_id][-1], data]
    if data == 'main menu':
        MESSAGES2DELETE[chat_id].append(message.message_id)
        delete_all_messages(chat_id)
        text = Template.objects.get(title='start').text.replace('FULL_NAME', user.full_name)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn_1 = Template2Button.objects.get(title='btn-1').text
        btn_2 = Template2Button.objects.get(title='btn-2').text
        keyboard.add(
         types.KeyboardButton('🗂 Каталог'),
         types.KeyboardButton('🛒 Корзина'),
         types.KeyboardButton('📦 Заказы'),
         types.KeyboardButton(btn_1),
         types.KeyboardButton(btn_2),
        )

        msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        MESSAGES2DELETE[chat_id].append(msg.message_id)
    elif data == 'categorys':
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        text = 'Выберите категорию'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboards_list = []
        
        for category in Category.objects.filter(parent=None):
            keyboards_list.append(
                types.InlineKeyboardButton(text=category.name, callback_data=f'CATEGORY|{category.id}')
            )
        for category in Category1.objects.filter(parent=None):
            keyboards_list.append(
                types.InlineKeyboardButton(text=category.name, callback_data=f'category|{category.id}')
            )
        keyboard.add(*keyboards_list)
        keyboard.add(
                types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
            )
        msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        delete_all_messages(chat_id)     
    elif 'category' in data.split('|')[0]:
        delete_all_messages(chat_id)
        category_id = data.split('|')[1]
        category = Category1.objects.get(id=category_id)
        text = f'Категория <b>{category.name}</b>'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboards_list = []
        if len(Category1.objects.filter(parent=category)) > 0:
            for c in Category1.objects.filter(parent=category):
                keyboards_list.append(
                    types.InlineKeyboardButton(text=c.name, callback_data=f'category|{c.id}')
                )
        if len(category.products.all()) > 0:
            for p in category.products.all():
                keyboards_list.append(
                    types.InlineKeyboardButton(text=p.title, callback_data=f'product|{p.id}')
                )
        keyboard.add(*keyboards_list)
        if category.parent != None:
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'category|{category.parent.id}')
                )
        else:
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'categorys')
                )
        delete_all_messages(chat_id)
        try:
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=message.message_id, reply_markup=keyboard)
        except Exception as e:
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception:
                pass
            bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'CATEGORY' in data:
        delete_all_messages(chat_id)
        category_id = data.split('|')[1]
        category = Category.objects.get(id=category_id)
        text = f'Категория <b>{category.name}</b>'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboards_list = []
        if len(Category.objects.filter(parent=category)) > 0:
            for c in Category.objects.filter(parent=category):
                keyboards_list.append(
                    types.InlineKeyboardButton(text=c.name, callback_data=f'CATEGORY|{c.id}')
                )
        elif len(Product.objects.filter(category=category)) > 0:
            for p in Product.objects.filter(category=category):
                keyboards_list.append(
                    types.InlineKeyboardButton(text=p.title, callback_data=f'PRODUCT|{p.id}')
                )
        keyboard.add(*keyboards_list)
        if category.parent != None:
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'CATEGORY|{category.parent.id}')
                )
        else:
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'categorys')
                )
        delete_all_messages(chat_id)
        try:
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=message.message_id, reply_markup=keyboard)
        except Exception as e:
            try:
                bot.delete_message(chat_id, message.message_id)
            except Exception:
                pass
            bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'product'in data:
        _, product_id = data.split('|')
        product = Product.objects.get(id=product_id)
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass

        images = Image.objects.filter(product=product)
        if len(images) > 0:
            image = images[0]
            keyboard2images = types.InlineKeyboardMarkup(row_width=3)
            keyboard2images.add(
                types.InlineKeyboardButton(text='⬅️', callback_data=f'CHANGEIMAGE|{product_id}|{-1}'),
                types.InlineKeyboardButton(text=f'1/{len(images)}', callback_data='#'),
                types.InlineKeyboardButton(text='➡️', callback_data=f'CHANGEIMAGE|{product_id}|{1}'),
            )
            msg = bot.send_photo(chat_id, photo=image.image, reply_markup=keyboard2images)
            if chat_id not in MESSAGES2DELETE.keys():
                MESSAGES2DELETE[chat_id] = []
            MESSAGES2DELETE[chat_id].append(msg.message_id)

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        text = f"Товар: {product.title}\nКатегория: {product.category}\n\nОписание: {product.description}\n"
        
        prices = PriceAndTitle.objects.filter(product=product)
        for price in prices:
            price_count = ShopCard.objects.filter(user=user, price_model=price, status=False)
            if len(price_count) > 0:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price} ₽' + f'({price_count[0].count} шт.)', callback_data=f'ADD|{price.id}')
                )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price} ₽', callback_data=f'ADD|{price.id}')
                )
        shopcard_count = len(ShopCard.objects.filter(user=user, status=False))
        
        keyboard.add(
                types.InlineKeyboardButton(text=f'🛒 Корзина ({shopcard_count})', callback_data=f'SHOPCARD|{product_id}')
            )
        back_data = BACK[chat_id][0] if chat_id in BACK.keys() else 'main menu'

        keyboard.add(
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=back_data)
        )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'PRODUCT' in data:
        product_id = data.split('|')[1]
        product = Product.objects.get(id=product_id)
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass

        images = Image.objects.filter(product=product)
        if len(images) > 0:
            image = images[0]
            keyboard2images = types.InlineKeyboardMarkup(row_width=3)
            keyboard2images.add(
                types.InlineKeyboardButton(text='⬅️', callback_data=f'CHANGEIMAGE|{product_id}|{-1}'),
                types.InlineKeyboardButton(text=f'1/{len(images)}', callback_data='#'),
                types.InlineKeyboardButton(text='➡️', callback_data=f'CHANGEIMAGE|{product_id}|{1}'),
            )
            msg = bot.send_photo(chat_id, photo=image.image, reply_markup=keyboard2images)
            if chat_id not in MESSAGES2DELETE.keys():
                MESSAGES2DELETE[chat_id] = []
            MESSAGES2DELETE[chat_id].append(msg.message_id)

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        text = f"{product.title}\n{product.category}\n\n{product.description}\n"

        prices = PriceAndTitle.objects.filter(product=product)
        for price in prices:
            price_count = ShopCard.objects.filter(user=user, price_model=price, status=False)
            if len(price_count) > 0:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price} ₽' + f'({price_count[0].count} шт.)', callback_data=f'ADD|{price.id}')
                )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price} ₽', callback_data=f'ADD|{price.id}')
                )
        shopcard_count = len(ShopCard.objects.filter(user=user, status=False))
        
        keyboard.add(
                types.InlineKeyboardButton(text=f'🛒 Корзина ({shopcard_count})', callback_data=f'SHOPCARD|{product_id}')
            )
        keyboard.add(
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'CATEGORY|{product.category.id}')
        )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'ADD' in data:
        _, priceandtitle_id = data.split('|')
        price_model = PriceAndTitle.objects.get(id=priceandtitle_id)
        shop_card, success = ShopCard.objects.get_or_create(user=user, price_model=price_model, status=False)
        if success:
            pass
        shop_card.count += 1
        shop_card.save()
        product = price_model.product
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        text = f"Товар: {product.title}\nКатегория: {product.category}\n\nОписание: {product.description}\n"

        prices = PriceAndTitle.objects.filter(product=product)
        for price in prices:
            price_count = ShopCard.objects.filter(user=user, price_model=price, status=False)
            if len(price_count) > 0:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price}₽' + f'({price_count[0].count} шт.)', callback_data=f'ADD|{price.id}')
                )
            else:
                keyboard.add(
                    types.InlineKeyboardButton(text='Купить - ' + price.price_title + f' - {price.price}₽', callback_data=f'ADD|{price.id}')
                )
        shopcard_count = len(ShopCard.objects.filter(user=user, status=False))
        keyboard.add(
                types.InlineKeyboardButton(text=f'🛒 Корзина({shopcard_count})', callback_data=f'SHOPCARD|{product.id}')
            )
        keyboard.add(
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'CATEGORY|{product.category.id}')
        )
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=keyboard)
    elif 'CHANGEIMAGE' in data:
        _, product_id, index = data.split('|')
        index = int(index)
        product = Product.objects.get(id=product_id)
        images = Image.objects.filter(product=product)
        if len(images) > 1:
            if index == -1:
                index = len(images)-1
            elif index >= len(images):
                index = 0 
            image = images[index]
            keyboard2images = types.InlineKeyboardMarkup(row_width=3)
            keyboard2images.add(
                types.InlineKeyboardButton(text='⬅️', callback_data=f'CHANGEIMAGE|{product_id}|{index-1}'),
                types.InlineKeyboardButton(text=f'{index+1}/{len(images)}', callback_data='#'),
                types.InlineKeyboardButton(text='➡️', callback_data=f'CHANGEIMAGE|{product_id}|{index+1}'),
            )
            new_photo = telebot.types.InputMediaPhoto(image.image)
            bot.edit_message_media(chat_id=chat_id, message_id=message.message_id, media=new_photo, reply_markup=keyboard2images)
    elif 'PLUS' in data or 'MINUS' in data:
        shop_card_id = data.split('|')[1]
        shop_card = ShopCard.objects.get(id=shop_card_id, status=False)
        if shop_card.count == 1 and 'MINUS' in data:
            shop_card.delete()
        else:
            if 'PLUS' in data:
                shop_card.count += 1
            else:
                shop_card.count -= 1
            shop_card.save()
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        delete_all_messages(chat_id)
        _, back_data = data.split('|')
        text = '<b>Корзина</b>\n'
        shopcard = ShopCard.objects.filter(user=user, status=False)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        summa = 0
        if len(shopcard) > 0:
            for i, el in enumerate(shopcard, 1):
                text += f'\n{i}. <b>{el.price_model.product.title}</b>\n{el.price_model.price_title} - {el.count} шт х {el.price_model.price}₽'
                summa += el.count * el.price_model.price
                keyboard.add(
                    types.InlineKeyboardButton(text=f'{i}. ++', callback_data=f'PLUS|{el.id}'),
                    types.InlineKeyboardButton(text=f'{i}. --', callback_data=f'MINUS|{el.id}'),
                )
            bonus = 0
            if summa >= 60_000:
                bonus = 10
            elif summa >= 50_000:
                bonus = 9
            elif summa >= 40_000:
                bonus = 8
            elif summa >= 30_000:
                bonus = 7
            elif summa >= 20_000:
                bonus = 6
            elif summa >= 15_000:
                bonus = 5
            elif summa >= 11_000:
                bonus = 4
            elif summa >= 7_000:
                bonus = 3
            elif summa >= 4000:
                bonus = 2
            else:
                bonus = 1
            text += f'\n\n<b>Бонусные семена</b> {bonus} шт.'
            text += f'\n\n<b>Итог: {summa} ₽</b>\n\n'
            keyboard.add(
                    types.InlineKeyboardButton(text=f'✅ Оформить заказ', callback_data=f'BUY'),
                )
        else:
            text += 'Корзина пусто'
        keyboard.add(
                types.InlineKeyboardButton(text=f'Меню', callback_data=f'main menu'),
            )

    
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)  
    elif 'SHOPCARD' in data:
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        delete_all_messages(chat_id)
        _, back_data = data.split('|')
        text = '<b>🛒 Корзина</b>\n\nℹ️ Список товаров:\n'
        shopcard = ShopCard.objects.filter(user=user, status=False)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        summa = 0
        if len(shopcard) > 0:
            for i, el in enumerate(shopcard, 1):
                text += f'\n{i}. <b>{el.price_model.product.title}</b>\n{el.price_model.price_title} - {el.count} шт х {el.price_model.price} ₽'
                summa += el.count * el.price_model.price
                keyboard.add(
                    types.InlineKeyboardButton(text=f'{i}. ++', callback_data=f'PLUS|{el.id}'),
                    types.InlineKeyboardButton(text=f'{i}. --', callback_data=f'MINUS|{el.id}'),
                )
            bonus = 0
            if summa >= 60_000:
                bonus = 10
            elif summa >= 50_000:
                bonus = 9
            elif summa >= 40_000:
                bonus = 8
            elif summa >= 30_000:
                bonus = 7
            elif summa >= 20_000:
                bonus = 6
            elif summa >= 15_000:
                bonus = 5
            elif summa >= 11_000:
                bonus = 4
            elif summa >= 7_000:
                bonus = 3
            elif summa >= 4000:
                bonus = 2
            else:
                bonus = 1
            text += f'\n\n<b>🎁 Бонусная семечка</b> {bonus} шт. 0 ₽'
            text += f'\n\n<b>Итогo: {summa} ₽</b>\n\n'
            text += f'\nℹ️ Пользуйтесь меню ниже, что бы увеличить/уменьшить количество товаров'
            keyboard.add(
                    types.InlineKeyboardButton(text=f'✅ Оформить заказ', callback_data=f'BUY'),
                )
        else:
            text += 'Корзина пусто'
        keyboard.add(
                types.InlineKeyboardButton(text=f'↩️ Назад', callback_data=f'main menu'),
            )

    
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif data == 'BUY':
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        delete_all_messages(chat_id)
        text = 'Выберите способ доставки'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        delivery_1 = Template2Button.objects.get(title='Почта России').text
        delivery_2 = Template2Button.objects.get(title='курьер').text
        delivery_3 = Template2Button.objects.get(title='самовывоз').text
        keyboard.add(
            types.InlineKeyboardButton(text=delivery_1, callback_data=f'DELIVERY|Почта России'),
            types.InlineKeyboardButton(text=delivery_2, callback_data=f'DELIVERY|курьер'),
            types.InlineKeyboardButton(text=delivery_3, callback_data=f'DELIVERY|самовывоз'),
        )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'DELIVERY' in data:
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        delete_all_messages(chat_id)
        delivery = Template2Button.objects.get(title=data.split('|')[1]).text
        user.delivery = delivery
        user.save()
        text = Template.objects.get(title='form').text
        
        if chat_id not in MESSAGES2DELETE.keys():
            MESSAGES2DELETE[chat_id] = []
        if user.info:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Изменить 📝', callback_data='EDIT_FORM'))
            keyboard.add(types.InlineKeyboardButton(text='Подтвердить форму ✅', callback_data='buy'))
            bot.send_message(chat_id, user.info, reply_markup=keyboard, disable_web_page_preview=True)
        else:
            msg = bot.send_message(chat_id, text, disable_web_page_preview=True)
            MESSAGES2DELETE[chat_id].append(msg.message_id)
            STATES[chat_id] = input_form
    elif data == 'EDIT_FORM':
        try:
            bot.delete_message(chat_id, message.message_id)
            
        except Exception:
            pass
        text = Template.objects.get(title='form').text
        msg = bot.send_message(chat_id, text, disable_web_page_preview=True)
        MESSAGES2DELETE[chat_id].append(msg.message_id)
        STATES[chat_id] = input_form
    elif data == 'buy':
        try:
            bot.delete_message(chat_id, message.message_id)
            
        except Exception:
            pass
        text = '<b>ℹ️ Список товаров:</b>\n'
        shopcard = ShopCard.objects.filter(user=user, status=False)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        summa = 0
        if len(shopcard) > 0:
            for i, el in enumerate(shopcard, 1):
                text += f'\n{i}. <b>{el.price_model.product.title}</b>\n{el.price_model.price_title} - {el.count} шт х {el.price_model.price} ₽'
                summa += el.count * el.price_model.price
                keyboard.add(
                    types.InlineKeyboardButton(text=f'{i}. ++', callback_data=f'PLUS|{el.id}'),
                    types.InlineKeyboardButton(text=f'{i}. --', callback_data=f'MINUS|{el.id}'),
                )
            bonus = 0
            if summa >= 60_000:
                bonus = 10
            elif summa >= 50_000:
                bonus = 9
            elif summa >= 40_000:
                bonus = 8
            elif summa >= 30_000:
                bonus = 7
            elif summa >= 20_000:
                bonus = 6
            elif summa >= 15_000:
                bonus = 5
            elif summa >= 11_000:
                bonus = 4
            elif summa >= 7_000:
                bonus = 3
            elif summa >= 4000:
                bonus = 2
            else:
                bonus = 1
            text += f'\n\n<b>🎁 Бонусная семечка</b> {bonus} шт. 0 ₽'
        text += '\n\n' + f'<b>Данные получателя:</b>\n\n{user.info.strip()}\n\n<b>Способ доставки:</b>\n\n' + str(user.delivery)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text='Оплатить 💳', callback_data=f'SAVEPURCHASE'),
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')

        )
        delivery = Template2Button.objects.get(text=str(user.delivery))
        delivery = Template.objects.get(title=delivery.title)
        text += f'\n\n<b>Итогo: {summa + float(delivery.text)} ₽</b>\n\n❗️ Проверьте, пожалуйста, данные перед оплатой.'
        msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        if chat_id not in MESSAGES2DELETE.keys():
            MESSAGES2DELETE[chat_id] = []
        MESSAGES2DELETE[chat_id].append(msg.message_id)
    elif data == 'SAVEPURCHASE':
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        text2purchase = message.text.replace('❗️ Проверьте, пожалуйста, данные перед оплатой.', '').replace('🛒 Корзина', '')
        shopcards = ShopCard.objects.filter(user=user, status=False)
        if len(shopcards) > 0:
            purchase = Purchase.objects.create(user=user, text=text2purchase)
            cash = 0
            for i in shopcards:
                cash += i.price_model.price*i.count
                i.status = True
                i.save()
                purchase.products.add(i)
                purchase.save()
            cash += int(Template.objects.get(title=Template2Button.objects.get(text=user.delivery).title).text)
            purchase.cash=cash
            purchase.save()
            text = Template.objects.get(title='requisites').text.replace('SUM', str(cash))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton(text='Отправить чек', callback_data=f'INPUT_CHECK|{purchase.id}')
            )
            bot.send_message(chat_id, text, reply_markup=keyboard)
        else:
            text += 'Корзина пусто'
            keyboard.add(
                types.InlineKeyboardButton(text=f'↩️ Назад', callback_data=f'main menu'),
            )
            bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif 'INPUT_CHECK' in data:
        purchase_id = data.split('|')[1]
        purchase = Purchase.objects.get(id=purchase_id)
        PURCHASES_ID[chat_id] = purchase_id
        STATES[chat_id] = input_check
        text = Template.objects.get(title='input check').text
        msg = bot.send_message(chat_id, text)

        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        if chat_id not in MESSAGES2DELETE.keys():
            MESSAGES2DELETE[chat_id] = []
        MESSAGES2DELETE[chat_id].append(msg.message_id)

def input_check(message):
    global MESSAGES2DELETE
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if chat_id in PURCHASES_ID.keys():
        file_id = None

    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        # Если это фотография, получите наилучшее качество (последнюю фотографию в списке)
        file_id = message.photo[-1].file_id

    if file_id:
        # Получите информацию о файле и URL для его скачивания
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        # Теперь у вас есть URL файла, который вы можете использовать для скачивания

        # Генерируйте уникальное имя файла, чтобы избежать конфликтов
        mime_type, _ = mimetypes.guess_type(file_url)

        # Получите расширение файла из URL
        file_extension = os.path.splitext(file_url)[1]

        # Генерируйте уникальное имя файла, используя slugify и добавьте расширение
        filename = slugify(file_info.file_path) + file_extension

        # Далее сохраните файл в поле FileField модели Django
        your_model_instance = Purchase.objects.get(id=PURCHASES_ID[chat_id])
        # Загрузите файл с помощью Django File
        your_model_instance.payment_check.save(filename, ContentFile(requests.get(file_url).content))
        your_model_instance.save()
        text = Template.objects.get(title='check').text
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
        )
        msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        

        
    else:
        text = f'Упс, что то пошло не так.'
    
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
        )
        msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
    delete_all_messages(chat_id)
    if chat_id not in MESSAGES2DELETE.keys():
        MESSAGES2DELETE[chat_id] = []
    MESSAGES2DELETE[chat_id].append(msg.message_id)
        


def input_form(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    text = f'{message.text}\n\n'
    user.info = text
    user.save()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(text='Изменить', callback_data=f'EDIT_FORM'),
        types.InlineKeyboardButton(text='Подтвердить', callback_data=f'buy'),
    )
    bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
    delete_all_messages(chat_id)

@bot.message_handler(commands=['start'])
def start_message_handler(message):
    global MESSAGES2DELETE
    chat_id = message.chat.id
    delete_all_messages(chat_id)
    if chat_id not in MESSAGES2DELETE.keys():
        MESSAGES2DELETE[chat_id] = []
    #MESSAGES2DELETE[chat_id].append(message.message_id)
    text = message.text
    user, success = BotUser.objects.get_or_create(chat_id=chat_id)
    if success:
        name = message.from_user.first_name
        user.full_name = name
        user.save()
    text = Template.objects.get(title='start').text.replace('FULL_NAME', user.full_name)
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_1 = Template2Button.objects.get(title='btn-1').text
    btn_2 = Template2Button.objects.get(title='btn-2').text
    keyboard.add(
         types.KeyboardButton('🗂 Каталог'),
         types.KeyboardButton('🛒 Корзина'),
         types.KeyboardButton('📦 Заказы'),
         types.KeyboardButton(btn_1),
         types.KeyboardButton(btn_2),
    )
    msg = bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    MESSAGES2DELETE[chat_id].append(msg.message_id)

   
@bot.message_handler(content_types=['text', 'photo', 'document'])
def message_handler(message):
    global STATES
    global MESSAGES2DELETE
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if chat_id not in MESSAGES2DELETE.keys():
        MESSAGES2DELETE[chat_id] = []
    MESSAGES2DELETE[chat_id].append(message.message_id)
    text = message.text
    btns = Template2Button.objects.filter(text=text)
    user = BotUser.objects.get(chat_id=chat_id)
    if text == '🗂 Каталог':
        text = 'Выберите категорию'
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboards_list = []
        for category in Category.objects.filter(parent=None):
            keyboards_list.append(
                types.InlineKeyboardButton(text=category.name, callback_data=f'CATEGORY|{category.id}')
            )
        for category in Category1.objects.filter(parent=None):
            keyboards_list.append(
                types.InlineKeyboardButton(text=category.name, callback_data=f'category|{category.id}')
            )
        keyboard.add(*keyboards_list)
        keyboard.add(
                types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
            )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        delete_all_messages(chat_id)
    elif text == '🛒 Корзина':
        try:
            bot.delete_message(chat_id, message.message_id)
        except Exception:
            pass
        delete_all_messages(chat_id)
        text = '<b>🛒 Корзина</b>\n\nℹ️ Список товаров:\n'
        shopcard = ShopCard.objects.filter(user=user, status=False)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        summa = 0
        if len(shopcard) > 0:
            for i, el in enumerate(shopcard, 1):
                text += f'\n{i}. <b>{el.price_model.product.title}</b>\n{el.price_model.price_title} - {el.count} шт х {el.price_model.price} ₽'
                summa += el.count * el.price_model.price
                keyboard.add(
                    types.InlineKeyboardButton(text=f'{i}. ++', callback_data=f'PLUS|{el.id}'),
                    types.InlineKeyboardButton(text=f'{i}. --', callback_data=f'MINUS|{el.id}'),
                )
            bonus = 0
            if summa >= 60_000:
                bonus = 10
            elif summa >= 50_000:
                bonus = 9
            elif summa >= 40_000:
                bonus = 8
            elif summa >= 30_000:
                bonus = 7
            elif summa >= 20_000:
                bonus = 6
            elif summa >= 15_000:
                bonus = 5
            elif summa >= 11_000:
                bonus = 4
            elif summa >= 7_000:
                bonus = 3
            elif summa >= 4000:
                bonus = 2
            else:
                bonus = 1
            text += f'\n\n<b>🎁 Бонусная семечка </b> {bonus} шт. 0 ₽'
            text += f'\n\n<b>Итог: {summa} ₽</b>'
            text += f'\nℹ️ Пользуйтесь меню ниже, что бы увеличить/уменьшить количество товаров'
            keyboard.add(
                    types.InlineKeyboardButton(text=f'✅ Оформить заказ', callback_data=f'BUY'),
                )
        else:
            text = '🛒 Корзина\n\nКорзина пуста'
        keyboard.add(
            types.InlineKeyboardButton(text=f'↩️ Назад', callback_data=f'main menu'),
        )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif text == '📦 Заказы': 
        text = '📦 Заказы\n\n'
        for i, p in enumerate(Purchase.objects.filter(user=user), 1):
            text += f'{i}) ЗАКАЗ № {p.id}. Статус заказа: {p.status}. {str(p.created).split()[0]}\n'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
                types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
            )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        delete_all_messages(chat_id)
    elif text == "⚙️ Настройки":
        text = '<b>Ваши настройки:</b>'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
                types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
            )
        bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
        delete_all_messages(chat_id)
    elif len(btns) > 0:
        btn = btns[0]
        if btn.title == "btn-1":
            text = Template.objects.get(title='btn-1').text
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
                )
            bot.send_message(chat_id, text, reply_markup=keyboard)
            delete_all_messages(chat_id)
        elif btn.title == "btn-2":
            text = Template.objects.get(title='btn-2').text
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                    types.InlineKeyboardButton(text='↩️ Назад', callback_data=f'main menu')
                )
            bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)
            delete_all_messages(chat_id)
    elif chat_id in STATES.keys():
        STATES[chat_id](message)
        del STATES[chat_id]
    


    
def run_schedule(): 
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(5).seconds.do(schedule_checker)
schedule_thread = Thread(target=run_schedule)
schedule_thread.start()

bot.infinity_polling()