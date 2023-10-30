from django.contrib import admin
from django.db import models
from .models import BotUser, Template, Template2Button, Category, Product, PriceAndTitle, Image, ShopCard, Category1, Load, Mailing, Purchase
from django.forms import CheckboxSelectMultiple, SelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'chat_id']

@admin.register(Template)
class TemlateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text']
    list_editable = ['text']

@admin.register(Template2Button)
class Template2ButtonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text']
    list_editable = ['text']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'created']
    list_filter = ['parent']

@admin.register(Category1)
class Category1Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'created']
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('товары', is_stacked=False)},
    }


class PriceAndTitle(admin.TabularInline):
    model = PriceAndTitle
    extra = 0

class Image(admin.TabularInline):
    model = Image
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'category']
    list_filter = ['category']
    inlines = [
            PriceAndTitle,
            Image
        ]
    search_fields = ['title']

""" @admin.register(ShopCard)
class ShopCardAdmin(admin.ModelAdmin):
    list_display = ['price_model', 'count', 'user', 'status'] """

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cash', 'payment_check', 'status', 'created']
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('товары', is_stacked=False)},
    }

class LoadAdmin(admin.TabularInline):
    model = Load
    extra = 0


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['message_text_ru', 'sent', 'datetime']
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Пользователи', is_stacked=False)},
    }
    inlines = [
        LoadAdmin,
    ]
    
