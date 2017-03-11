from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ITEnergy import bot


class Product(models.Model):
    name = models.CharField('Название', max_length=64)
    price = models.DecimalField('Стоимость', max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class Order(models.Model):
    cart = models.ManyToManyField(Product)
    name = models.CharField('ФИО заказчика', max_length=128)
    tel_number = models.CharField('Номер телефона', max_length=15)

    # tel_number = phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
    # error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    class Meta:
        abstract = True


class DeliveryOrder(Order):
    address = models.CharField('Адрес', max_length=128)
    date_delivery = models.DateTimeField('Дата доставки')

    def __str__(self):
        return 'Для {} от {} '.format(self.name, self.date_delivery.strftime("%d.%m.%Y %H:%M:%S"))

    class Meta:
        verbose_name = 'Заказ на доставку'
        verbose_name_plural = 'Заказы на доставку'


class ReservationOrder(Order):
    date_visit = models.DateTimeField()
    count_visitors = models.PositiveSmallIntegerField('Количество посетителей')
    number_place = models.PositiveSmallIntegerField('Номер стола')

    def __str__(self):
        return 'В {} на {}, место #{} '.format(self.date_visit.strftime("%d.%m.%Y %H:%M:%S"), self.count_visitors,
                                               self.number_place)

    class Meta:
        verbose_name = 'Заявка на бронирование'
        verbose_name_plural = 'Заявки на бронирование'


class Employee(models.Model):
    name = models.CharField('ФИО', max_length=128)
    chat_id = models.CharField('ID Telegram', max_length=32, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DeliveryStaff(Employee):
    actual_order = models.OneToOneField(DeliveryOrder, null=True, blank=True)
    __original_is_verified = False

    def __init__(self, *args, **kwargs):
        super(DeliveryStaff, self).__init__(*args, **kwargs)
        self.__original_is_verified = self.is_verified

    class Meta:
        verbose_name = 'Служба доставки'
        verbose_name_plural = 'Служба доставки'


@receiver(post_save, sender=DeliveryStaff)
def do_something_when_user_updated(sender, instance, created, **kwargs):
    if not created and instance.is_verified != instance.__original_is_verified:
        if instance.is_verified:
            bot.send_message(chat_id=instance.chat_id,
                             text='Ваш статус подтвержден')
        else:
            bot.send_message(chat_id=instance.chat_id,
                             text='Ваш статус аннулирован')
        pass
