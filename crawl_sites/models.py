from django.db import models

# Create your models here.
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, help_text="Enter manufacturer name.")

    class Meta:
        db_table = 'manufacturer'
        ordering = ['name']

    def __str__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=60, help_text="Enter webiste name.")

    class Meta:
        db_table = 'website'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, help_text='Enter product name.')
    size = models.CharField(max_length=100, null=False, help_text='Size, weight, package count, etc.')

    class Meta:
        db_table = 'product'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.size})'

class Website_Product(models.Model):
    website = models.ForeignKey(Website, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    url = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'website_product'

    def __str__(self):
        return self.url