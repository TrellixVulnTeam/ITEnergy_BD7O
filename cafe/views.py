from random import randint

from dateutil import parser
from django.shortcuts import render

from ITEnergy import bot
from cafe.models import DeliveryOrder, DeliveryStaff

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
    return render(request, 'index.html')


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
    input_name = request.POST.get('inputNameTwo', '')
    input_number = request.POST.get('inputNumberTwo', '')
    input_address = request.POST.get('inputAdress', '')
    coffee = request.POST.getlist('coffee_type')
    input_date = request.POST.get('inputDateTwo', '')
    input_time = request.POST.get('inputTimeTwo', '')

    datetime = parser.parse(input_date + ' ' + input_time)

    free_staff = DeliveryStaff.objects.filter(actual_order__isnull=True)
    if free_staff.count() > 0:
        random_index = randint(0, free_staff.count() - 1)
        selected_staff = free_staff[random_index]
        order = DeliveryOrder(date_delivery=datetime.strftime("%d.%m.%Y %H:%M:%S"), address=input_address,
                              name=input_name, tel_number=input_number)
        order.save()
        selected_staff.actual_order = order
        selected_staff.save()
        if len(coffee) > 1:
            bot.send_message(chat_id=selected_staff.chat_id,
                             text='{} заказал такой список товаров: {}.\nДата: {}.\nТелефон: {}.\nАдрес: {}'.format(
                                 input_name, ', '.join(coffee), datetime.strftime("%d.%m.%Y %H:%M:%S"), input_number,
                                 input_address))
        else:
            bot.send_message(chat_id=selected_staff.chat_id,
                             text='{} заказал {}.\nДата: {}.\nТелефон: {}.\nАдрес: {}'.format(
                                 input_name, ', '.join(coffee), datetime.strftime("%d.%m.%Y %H:%M:%S"), input_number,
                                 input_address))
    else:
        bot.send_message(chat_id='@coffeelab_reserv',
                         text='Не хвататет работников доставки:(')

    return render(request, 'thanks.html')
