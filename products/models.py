from django.db   import models

from core.models import TimeStampModel

class Category(TimeStampModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'
        
class Tag(TimeStampModel):
    name    = models.CharField(max_length=50)
    type    = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'

class Product(TimeStampModel):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    is_sold     = models.BooleanField(default=False)
    badge       = models.CharField(max_length=50, null=True)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag         = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class Option(TimeStampModel):
    name    = models.CharField(max_length=50)
    size    = models.CharField(max_length=50)
    price   = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'