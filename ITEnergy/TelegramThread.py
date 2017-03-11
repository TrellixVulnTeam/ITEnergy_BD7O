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

        @self.bot.message_handler(commands=['no'])
        def decline(message):
            user = DeliveryStaff.objects.get(chat_id=message.from_user.id)
            if user.is_verified and user.actual_order is not None:
                user.actual_order = None
                user.save()
                self.bot.send_message(chat_id=user.chat_id, text="Заказ успешно отменен")

        self.bot.polling()
