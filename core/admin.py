from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Product, ReferenceCode, CartItem, Order


def export_as_csv(model_admin, request, queryset):
	with open('prods.csv', 'w') as f:
		f.write("title,description,id,current_price,previous_price,image,is_deal_of_the_week\n")
		for item in queryset:
			title = item.title
			id = item.product_id
			current_price = item.current_price
			previous_price = item.previous_price
			image = item.image.url
			is_deal_of_the_week = item.is_deal_of_the_week
			f.write(f"{title},{id},{current_price},{previous_price},{image},{is_deal_of_the_week}\n")


export_as_csv.short_description = 'Export as CSV'


class ProductAdmin(ModelAdmin):
	fields = ['title', 'description', 'product_id' , 'current_price', 'previous_price', 'label', 'category', 'image', 'is_deal_of_the_week']
	list_display = ['title', 'label','category', 'current_price']
	list_display_links = ['title']
	list_filter = ['is_deal_of_the_week', 'label']
	actions = [export_as_csv]
	list_editable = ['label', 'category']
	search_fields = ['title', 'product_id']
	readonly_fields = ['product_id']


class CartItemAdmin(ModelAdmin):
	fields = ['product', 'quantity', 'is_ordered']
	list_display = ['product', 'quantity', 'is_ordered']
	readonly_fields = ['quantity', 'is_ordered']


class OrderAdmin(ModelAdmin):
	fields = ['items', 'reference_code', 'is_ordered', 'is_being_processed', 'is_delivered', 'is_recieved', 'refund_requested', 'refund_granted']
	list_display = ['__str__', 'is_ordered', 'is_being_processed', 'is_delivered', 'is_recieved', 'refund_requested', 'refund_granted']
	readonly_fields = ['reference_code']


admin.site.register(Product, ProductAdmin)
admin.site.register(ReferenceCode)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)


