from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    chat_id = models.IntegerField(unique=True, verbose_name='Айди')
    full_name = models.CharField(max_length=255, verbose_name='Имя')
    delivery = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип доставка')
    info = models.TextField(null=True, blank=True, verbose_name='Инфо')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Template(models.Model):
    title = models.CharField(max_length=255, verbose_name='Не трогать!!')
    text = models.TextField(unique=True, 
    verbose_name='Текст')


    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def __str__(self) -> str:
        return self.title   

class Template2Button(models.Model):
    title = models.CharField(max_length=255, verbose_name='Не трогать!!')
    text = models.TextField(verbose_name='Текст')


    class Meta:
        verbose_name = 'кнопку(текст)'
        verbose_name_plural = 'кнопки(текст)'

    def __str__(self) -> str:
        return self.title   

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Названия')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительская категория')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    class Meta:
        verbose_name_plural = 'Сидбанки'

    def __str__(self):
        return self.name

class Category1(models.Model):
    name = models.CharField(max_length=100, verbose_name='Названия')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительская категория')
    products = models.ManyToManyField("Product", blank=True, verbose_name='Товары')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    class Meta:
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Товар')
    description = models.TextField(verbose_name='Описания')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка на товар')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
    
class Image(models.Model):
    product = models.ForeignKey(Product, verbose_name=("Товар"), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image', null=True, blank=True, verbose_name='Фото')

    
    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'

    def __str__(self):
        return str(self.product)

class PriceAndTitle(models.Model):
    product = models.ForeignKey(Product, verbose_name=("Товар"), on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    price_title = models.CharField(max_length=60, verbose_name='Текст')
    
    class Meta:
        verbose_name = 'цену'
        verbose_name_plural = 'цены'

    def __str__(self):
        return f'{self.product.title} {self.price_title}'

class ShopCard(models.Model):
    price_model = models.ForeignKey(PriceAndTitle, verbose_name=("Товар"), on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name='Кол-ва')
    user = models.ForeignKey(BotUser, verbose_name='пользователь', on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name='Статус')

    def __str__(self):
        return str(self.price_model)

class Purchase(models.Model):
    products = models.ManyToManyField("ShopCard", blank=True, verbose_name="Продукты")
    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('Оплачен', 'Оплачен'),
        ('Отправлен', 'Отправлен'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Ожидания', verbose_name='Статус оплаты')
    payment_check = models.FileField(upload_to='check', null=True, blank=True, verbose_name='Чек')
    cash = models.FloatField(default=0, verbose_name='Сумма')
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    text = models.TextField(verbose_name='тест')
    schedule = models.BooleanField(default=False, verbose_name='Уведомления клиенту')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
    def __str__(self):
        return f'ЗАКАЗ № {self.id}'
    


class Mailing(models.Model):
    message_text_ru = models.TextField(verbose_name='Текст')
    sent = models.BooleanField(default=False, verbose_name='Отправлено')
    datetime = models.DateTimeField(verbose_name=('Дата рассылки'))

    users_list = models.ManyToManyField(BotUser, blank=True, verbose_name=('Список пользователей'))
    class Meta:
        verbose_name = ('рассылку')
        verbose_name_plural = ('Рассылка')

    def __str__(self):
        return self.message_text_ru

    def get_users(self):
        users = []
        user_ids = list(self.users_list.all().values_list('id', flat=True))
        for u in list(BotUser.objects.filter(id__in=user_ids)):
            users.append(u)
            
        return users
    
class Load(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Фото'),
        ('video', 'Видео'),
        ('document', 'Документ'),
        ('audio', 'Аудио'),
    ]
    type_choice = models.CharField(max_length=20, choices=TYPE_CHOICES, default='photo', verbose_name='Выбор типа')
    file = models.FileField(upload_to='media/', verbose_name='Файл')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='loads')
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.type_choice
    