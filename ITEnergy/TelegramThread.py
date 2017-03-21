from threading import Thread

import django

from cafe.models import DeliveryStaff


class TelegramThread(Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot
        self.daemon = True
        self.start()

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            new = DeliveryStaff(name=message.from_user.first_name + " " + message.from_user.last_name,
                                chat_id=str(message.from_user.id), is_verified=False)
            try:
                new.save()
                self.bot.send_message(chat_id=new.chat_id,
                                      text="Здравствуйте, для работы в службе доставки необходимо получить доступ. "
                                           "Позвоните на номер 8 800 555 35 35")
            except django.db.utils.IntegrityError:
                if DeliveryStaff.objects.get(chat_id=new.chat_id).is_verified:
                    self.bot.send_message(chat_id=new.chat_id,
                                          text="С возвращением!")
                else:
                    self.bot.send_message(chat_id=new.chat_id,
                                          text="Здравствуйте, для работы в службе доставки необходимо получить доступ. "
                                               "Позвоните на номер 8 800 555 35 35")

        @self.bot.message_handler(commands=['get'])
        def accept(message):
            user = DeliveryStaff.objects.get(chat_id=message.from_user.id)
            if user.is_verified and user.actual_order is not None:
                user.orders_count += 1
                user.actual_order = None
                user.save()
                self.bot.send_message(chat_id=user.chat_id, text="Заказ успешно принят, удачного пути!")

        @self.bot.message_handler(commands=['no'])
        def decline(message):
            user = DeliveryStaff.objects.get(chat_id=message.from_user.id)
            if user.is_verified and user.actual_order is not None:
                user.orders_count += 1
                user.orders_decline += 1
                order = user.actual_order
                user.actual_order.declined_by.add(user)
                user.actual_order.save()
                user.actual_order = None
                user.save()
                self.bot.send_message(chat_id=user.chat_id, text="Заказ успешно отменен")

                staff = DeliveryStaff.objects.all()
                new = staff.exclude(id__in=order.declined_by.all())
                if new.count()>0:
                    selected_staff = new[0]
                    selected_staff.actual_order = order
                    selected_staff.save()

                    # if len(order) > 1:
                    #     bot.send_message(chat_id=selected_staff.chat_id,
                    #                      text='{} заказал такой список товаров: {}.\nТелефон: {}.\nАдрес: {}'.format(
                    #                          input_name, ', '.join(list_orders), input_number,
                    #                          input_address))
                    # else:
                    #     bot.send_message(chat_id=selected_staff.chat_id,
                    #                      text='{} заказал {}.\nТелефон: {}.\nАдрес: {}'.format(
                    #                          input_name, ', '.join(list_orders), input_number,
                    #                          input_address))
                    self.bot.send_message(chat_id=selected_staff.chat_id,
                                                text='{} заказал такой список товаров: {}.\nТелефон: {}.\nАдрес: {}'.format(
                                                'Игорь', '2 Каппучино', '0938700546',
                                                'Мой дом'))
                    self.bot.send_message(chat_id='@coffeelab_reserv',
                                 text='Никто не хочет брать заказ:( '+'id:'+str(order.id))

        self.bot.polling()
