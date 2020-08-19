from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType  # Для создания своего ключа каждому продукту
from django.contrib.contenttypes.fields import GenericForeignKey  #Внешний ключ



User = get_user_model() #говорим джанго что необходимо использовать юзера который указан в (settings.AUTH_USER_MODEL)-скрытая настройка в setttings



# Category
# Product
# CartProduct
# Cart
#Order
#***********************
# Customer
# Specification


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)   #/category/notebooks - slug = notebooks

    def __str__(self):
        return self.name

class Product(models.Model):

    class Meta:
        abstract = True #абстрактная модель нельзя создавать миграции

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')   #изображение товара
    description = models.TextField(verbose_name='Описание', null=True)  #Описание товара  null=True может быть пустым
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')    #цена  max_digits=9 колво цыфр    decimal_places=2 кол-во цыфр после запятой

    def __str__(self):
        return self.title

#Ноутбуки
#         
#Diagonal
#Display
#processor_freq
#Ram
#Video
#time_without_charge

class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_withour_charge = models.CharField(max_length=255, verbose_name='Время работы батареи')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)         

class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Обьем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный обьем встраиваемой памяти')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


    

#class Product(models.Model):

#     category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)  #on_delete=models как быть в случае удаления  CASCADE удалить все связи с обьектом
#     title = models.CharField(max_length=255, verbose_name='Наименование')
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(verbose_name='Изображение')    #изображение товара
#     description = models.TextField(verbose_name='Описание', null=True)   #Описание товара  null=True может быть пустым
#     price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')  #цена  max_digits=9 колво цыфр    decimal_places=2 кол-во цыфр после запятой
#
#     def __str__(self):
#         return self.title

#class CartProduct(models.Model):

#    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
#    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
#    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
#    qty = models.PositiveIntegerField(default=1)        #количество
#    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

#    def __str__(self):
#       return "Продукт:{} (для корзины)".format (self.product.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()   #идентификатор инстанса модели
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)        #количество
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
       return "Продукт:{} (для корзины)".format (self.product.title)


class Cart(models.Model):

    owner =  models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)    #Владелец корзины        
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')  #
    total_products = models.PositiveIntegerField(default=0) #показывать коректное кол-во товаров в корзине
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена') #окончательная, полная цена

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адресс')

    def __str__(self):
        return "Покупатель:{} {}".format (self.user.first_name, self.user.last_name)

#class Specifications(models.Model):

#   content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#    object_id = models.PositiveIntegerField()
#    product_name = models.CharField(max_length=255, verbose_name='Название товара')
#
#    def __str__(self):
#        return "Характеристики для товара: {}".format(self.name)
    


    









