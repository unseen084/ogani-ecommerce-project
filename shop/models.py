from django.db import models

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
    image = models.ImageField(upload_to="app/images/")
    price = models.FloatField()
    discounted_price = models.FloatField()
    fav_count = models.IntegerField()
    latest = models.DateField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)

    def __str__(self):
        return self.title
