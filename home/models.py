from django.db import models
STATUS = (('active','Active'),('','Default'))
LABELS = (('offer','Offer'),('new','New'),('hot','Hot'),('','Default'))
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 500, unique = True)
	image = models.ImageField(upload_to = 'media', null = True)
	status = models.CharField(choices = STATUS,max_length = 300,blank = True)
	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 500, unique = True)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Slider(models.Model):
	name = models.CharField(max_length = 300)
	url = models.URLField(max_length = 500)
	image = models.ImageField(upload_to = 'media', null = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,max_length = 300,blank = True)

	def __str__(self):
		return self.name

class Ad(models.Model):
	name = models.CharField(max_length = 300)
	url = models.URLField(max_length = 500)
	image = models.ImageField(upload_to = 'media', null = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,max_length = 300,blank = True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 500, unique = True)
	image = models.ImageField(upload_to = 'media', null = True)
	rank = models.IntegerField()
	status = models.CharField(choices = STATUS,max_length = 300,blank = True)
	price = models.FloatField()
	discounted_price = models.FloatField()
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
	description = models.TextField(blank = True)
	labels = models.CharField(choices = LABELS,max_length = 300,blank = True)

	def __str__(self):
		return self.name


class Cart(models.Model):
	username = models.CharField(max_length = 300)
	slug = models.CharField(max_length = 500)
	items = models.ForeignKey(Product,on_delete = models.CASCADE)
	quantity = models.IntegerField(default = 1)
	total = models.IntegerField(default = 1)
	checkout = models.BooleanField(default = False)

	def __str__(self):
		return self.name