from django.db import models
import string, random

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=255)

	def __str__(self):
        return str(self.title)

class SubCategory(models.Model):
	title = models.CharField(max_length=255)
	parent = models.ForeignKey(
		'Category',
		on_delete = models.CASCADE,
	)

	def __str__(self):
        return str(self.title)

class Item(models.Model):
	title = models.CharField(max_length=255)
	category = models.ForeignKey(
		'SubCategory',
		on_delete = models.CASCADE,
	)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	origin = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now = True)

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])

    def __str__(self):
        return str(self.title)

	
class ItemImage(models.Model):
	item = models.ForeignKey(
		Item,
		related_name='images'
	)
	image = models.ImageField()
	
				