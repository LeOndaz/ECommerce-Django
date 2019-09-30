
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Product(models.Model):
	LABEL_CHOICES = (
		('BS', 'Best Seller'),
		('N', 'New'),
		('OFS', 'Out of stock'),
		('C', 'Our Choice'),
		('F', 'Featured'),
		('OS', 'On Sale'),
	)

	CATEGORY_CHOICES = (
		('HP', 'Headphones'),
		('MOB', 'Mobile'),
		('TV', 'Television'),
		('PCP', 'Computer Part'),
		('TECH', 'Technology'),
	)

	title = models.CharField(max_length=120)
	description = models.TextField(default='dummy text dummy text dummy text dummy text dummy text')
	category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)

	product_id = models.SlugField(max_length=80, validators=[RegexValidator(regex='[A-Za-z0-9]{20}$')], blank=True, unique=True)

	previous_price = models.IntegerField(blank=True, null=True)
	current_price = models.IntegerField()
	is_deal_of_the_week = models.BooleanField(default=False, null=True)
	is_in_stock = models.BooleanField(default=True)
	image = models.ImageField(default='product_default.jpg', upload_to='products')
	label = models.CharField(max_length=3, choices=LABEL_CHOICES, null=True, blank=True)
	# how_many_sold = models.IntegerField()

	@staticmethod
	def get_deal_of_the_day_items_queryset():
		return Product.objects.filter(is_deal_of_the_week=True)

	@staticmethod
	def get_deal_of_the_day_items_count():
		return Product.get_deal_of_the_day_items_queryset().count()

	@staticmethod
	def get_available_quantity():
		return Product.objects.all().count()

	@staticmethod
	def get_specific_category_queryset(category):
		return Product.objects.filter(category=category)

	@staticmethod
	def get_featured_products_queryset():
		return Product.objects.filter(label='F')

	# def get_how_many_sold(self):
	# 	return self.how_many_sold


class CartItem(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	is_ordered = models.BooleanField(default=False)

	def get_quantity(self):
		return self.quantity

	def get_final_price(self):
		return self.quantity * self.product.current_price

	def get_discount(self):
		pass

	def __str__(self):
		return f"{self.product.title}"


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField('CartItem')
	reference_code = models.OneToOneField('ReferenceCode', related_name='product_code', on_delete=models.CASCADE, null=True)

	is_ordered = models.BooleanField(default=False)

	is_being_processed = models.BooleanField(default=False)
	is_delivered = models.BooleanField(default=False)
	is_recieved = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	def get_item_count(self):
		count = 0
		for i in range(self.items.all().count()):
			count += self.items.all()[i].quantity
		return count

	def get_total(self):
		total = 0
		for i in range(self.items.all().count()):
			total += self.items.all()[i].quantity * self.items.all()[i].product.current_price
		return total

	def __str__(self):
		return f"Order containing { self.get_item_count() } items"


class ReferenceCode(models.Model):
	code = models.CharField(validators=[RegexValidator(regex='[a-zA-Z0-9]{20}$', message='20 A-Z a-z 0-9')], max_length=20)

	def __str__(self):
		return self.code


