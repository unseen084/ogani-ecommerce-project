from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = (
    ('FM', 'Fresh Meat'),
    ('V', 'Vegetables'),
    ('F&N', 'Fruit & Nut Gifts'),
    ('FB', 'Fresh Berries'),
    ('OF', 'Ocean Foods'),
    ('B&E', 'Butter & Eggs'),
    ('FF', 'Fastfood'),
    ('FO', 'Fresh Onion'),
    ('P%C', 'Papayaya & Crisps'),
    ('OM', 'Oatmeal'),
    ('B', 'Fresh Bananas'),
)


class Product(models.Model):
    title = models.CharField(max_length=200)

    image1 = models.ImageField(upload_to="app/images/")
    image2 = models.ImageField(upload_to="app/images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="app/images/", null=True, blank=True)
    image4 = models.ImageField(upload_to="app/images/", null=True, blank=True)
    image5 = models.ImageField(upload_to="app/images/", null=True, blank=True)

    shortinfo = models.TextField(default='NA')
    description = models.TextField(default='NA')
    weight = models.FloatField(default=0.0)
    price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    fav_count = models.IntegerField(null=True, blank=True)
    latest = models.DateField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

