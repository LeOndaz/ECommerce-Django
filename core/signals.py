from django.dispatch import receiver
from django.db.models.signals import post_save
import base64
import os
import re
from random import choice
import string
from .models import ReferenceCode, Order, Product, CartItem
from django.utils.text import slugify


def generate_random_reference_code_order():
	code_unprocessed = base64.b64encode(os.urandom(20)).decode('ascii')[:20]
	code = re.sub('[^A-Za-z0-9]', choice(string.ascii_lowercase + string.ascii_letters + string.digits + string.ascii_uppercase), code_unprocessed)
	return ReferenceCode.objects.create(code=code)


def generate_random_product_id():
	return re.sub('[^A-Za-z0-9]', choice(string.ascii_lowercase + string.ascii_letters + string.digits + string.ascii_uppercase), base64.b64encode(os.urandom(20)).decode('ascii')[:20])


@receiver(post_save, sender=Order, dispatch_uid="unique_order")
def handler(sender, instance, created, **kwargs):
	if created:
		instance.reference_code = generate_random_reference_code_order()
		instance.save()


@receiver(post_save, sender=Product, dispatch_uid="unique_product")
def handler(sender, instance, created, **kwargs):
	if created:
		instance.product_id = generate_random_product_id() + '/' + slugify(instance.title)
		instance.save()