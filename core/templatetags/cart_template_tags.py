from django import template
from ..models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
	if user.is_authenticated:
		order_qs = Order.objects.filter(user=user, is_ordered=False)
		if order_qs.exists():
			if order_qs[0].get_item_count() != 0:
				return order_qs[0].get_item_count()
			else:
				return 'Empty'


@register.filter
def order_total(user):
	if user.is_authenticated:
		order_qs = Order.objects.filter(user=user, is_ordered=False)
		if order_qs.exists():
			return order_qs[0].get_total()

