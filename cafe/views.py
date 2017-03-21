from datetime import datetime
from random import randint

from dateutil import parser
from django.shortcuts import render

from ITEnergy import bot
from cafe.models import DeliveryOrder, DeliveryStaff, Product, Item
import json

word = ["человека", "человека", "человек"]


def get_com(x, y):
    inumber = x % 100
    if 11 <= inumber <= 19:
        return y[2]
    else:
        iinumber = inumber % 10
    if iinumber == 1:
        return y[0]
    elif iinumber == 2 or iinumber == 3 or iinumber == 4:
        return y[1]
    else:
        return y[2]


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def reserve_place(request):
    input_name = request.POST.get('inputName', '')
    input_number = request.POST.get('inputNumber', '')
    input_count = int(request.POST.get('inputCount', '0'))
    input_date = request.POST.get('inputDate', '')
    input_time = request.POST.get('inputTime', '')

    input_datetime = parser.parse(input_date + ' ' + input_time)

    bot.send_message(chat_id='@coffeelab_reserv',
                     text='{} забронировал место на {} {}.\nДата: {}.\nТелефон: {}.'.format(
                         input_name, input_count, get_com(input_count, word), str(input_datetime), input_number))

    return render(request, 'thanks.html')


def buy_coffee(request):
    #{'price': 45, 'site': '127.0.0.1:8000', 'currency': '₽', 'language': 'russian', 'name': 'df', 'phone': '23', 'address': 'sdf', 'items': [{'name': 'americano', 'price': 45, 'quantity': 1}]}
    data = request.POST.get('data', '')
    data = json.loads(data)
    input_name = data['name']
    input_number = data['phone']
    input_address = data['address']
    orders = data['items']
    list_orders = []
    free_staff = DeliveryStaff.objects.filter(actual_order__isnull=True, is_verified=True)
    if free_staff.count() > 0:
        random_index = randint(0, free_staff.count() - 1)
        selected_staff = free_staff[random_index]
        delivery_orders = DeliveryOrder(address=input_address, name=input_name, tel_number=input_number, date_ordered=datetime.now())
        full_price = 0
        for order in orders:
            name = order['name']
            quantity = order['quantity']
            product = Product.objects.get(name_id=name)
            item = Item(product=product, quantity=quantity, order=delivery_orders)
            full_price += item.total_price
            list_orders.append(str(order['quantity'])+" "+product.name)

        delivery_orders.save()
        selected_staff.actual_order = delivery_orders
        selected_staff.save()

        if len(orders) > 1:
            bot.send_message(chat_id=selected_staff.chat_id,
                             text='{} заказал такой список товаров: {}.\nТелефон: {}.\nАдрес: {}'.format(
                                 input_name, ', '.join(list_orders), input_number,
                                 input_address))
        else:
            bot.send_message(chat_id=selected_staff.chat_id,
                             text='{} заказал {}.\nТелефон: {}.\nАдрес: {}'.format(
                                 input_name, ', '.join(list_orders), input_number,
                                 input_address))
    else:
        bot.send_message(chat_id='@coffeelab_reserv',
                         text='Не хвататет работников доставки:(')

    return render(request, 'thanks.html')
