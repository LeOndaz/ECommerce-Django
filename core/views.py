from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Product, CartItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class MainPageView(View):
	def get(self, *args, **kwargs):

		return render(self.request, 'core/index.html', {
			'PRODUCT': Product,
			'featured_products': Product.get_featured_products_queryset(),
			'deal_of_the_day_products': Product.get_deal_of_the_day_items_queryset()
		})


class ShopView(ListView):
	paginate_by = 15
	model = Product
	template_name = 'core/shop.html'
	# TODO : IF YOU EDIT GET, PASS CONTEXT OTHERWISE LEAVE IT BE


class ProductDetailView(DetailView):
	model = Product
	template_name = "core/product.html"
	context_object_name = "product"
	slug_field = 'product_id'
	slug_url_kwarg = 'product_id'


class CartView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):

		total = 0
		for order in Order.objects.filter(user=self.request.user, is_ordered=False):
			total += order.get_total()

		return render(self.request, 'core/cart.html', {
			'orders': Order.objects.filter(user=self.request.user, is_ordered=False).all(),
			'ORDER_TOTAL': total,

		})


class AddToCartView(LoginRequiredMixin, View):
	def post(self, *args, **kwargs):
		print(self.request.POST)
		try:
			product_id = self.request.POST['product_id']
		except:
			return redirect('/')

		product = Product.objects.get(product_id=product_id)
		order_qs = Order.objects.filter(user=self.request.user, is_ordered=False)
		print('working here')
		if order_qs.exists():
			order = order_qs[0]
			# he has an existing order we must check if there's an item we added in it
			try:
				cart_item = order.items.get(product=product, is_ordered=False)
				cart_item.quantity += 1
				cart_item.save()
				order.save()
				print('2nd part')
				# QUANTITY INCREASE ( USE AJAX TO RAISE IT IN FRONT END )
				return HttpResponse('QT', status=204)

			except ObjectDoesNotExist:
				cart_item = CartItem.objects.create(product=product)
				cart_item.save()
				order.items.add(cart_item)
				order.save()
				print('3rd part')
				# CART ITEM CREATED
				return HttpResponse('CTC', status=204)
		else:
			order = Order.objects.create(user=self.request.user)
			cart_item = CartItem.objects.create(product=product)
			order.items.add(cart_item)
			cart_item.save()
			order.save()
			# ORDER CREATED , USE AJAX TO BLA BLA BLA
			print('4th part')
			return HttpResponse('CTC', status=204)


class RemoveFromCartView(LoginRequiredMixin, View):
	def post(self, *args, **kwargs):
		print(self.request.POST)
		try:
			product_id = self.request.POST['product_id']
		except:
			return redirect('/')

		product = Product.objects.get(product_id=product_id)
		order_qs = Order.objects.filter(user=self.request.user, is_ordered=False)
		if order_qs.exists():
			order = order_qs[0]
			cart_item = order.items.get(product=product, is_ordered=False)
			print('working')
			if cart_item.quantity == 1:
				print('2')
				cart_item.delete()
				order.save()
				# delete item from cart
				return JsonResponse({'quantity': '0'})
			else:
				print('2')
				cart_item.quantity -= 1
				cart_item.save()
				order.save()
				return JsonResponse({
					'quantity': str(cart_item.quantity),
					'cart_item_total': str(cart_item.get_final_price()),
					'order_total': str(order.get_total())
				})
		else:
			return HttpResponse('No order')


class CartDetailsAPI(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			order_qs = Order.objects.filter(user=self.request.user, is_ordered=False)
			if order_qs.exists():
				data = {
					'total': order_qs[0].get_total(),
					'count': order_qs[0].get_item_count(),
				}
				return JsonResponse(data)
