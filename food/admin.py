# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .models import (Blog, Product, Categorie, OrderLine, Order, Recipe,
                     ProductDetail, Doctor, Manufacturer, Payment, Contact,
                     Comment, health_problem, User, RecipeRating, Allergie,
                     Customer, Subscriber, Post, Replay, RecipeComment,
                     RecipeCommentReplay,
                     ProductCategory, CommentProduct, CustomerProduct, BloodType, DietType, ActivityLevel, ProductArt)

for c in [RecipeComment, Recipe, RecipeCommentReplay, RecipeRating]:
    admin.site.register(c)

admin.site.register(CustomerProduct)
admin.site.register(CommentProduct)
admin.site.register(ProductCategory)
admin.site.register(User)
admin.site.register(Replay)
admin.site.register(Payment)
admin.site.register(Post)
admin.site.register(Subscriber)
admin.site.register(Contact)
admin.site.register(Blog)
admin.site.register(Product)
admin.site.register(Categorie)
admin.site.register(OrderLine)
admin.site.register(Order)
admin.site.register(ProductDetail)
admin.site.register(Doctor)
admin.site.register(Manufacturer)
admin.site.register(Comment)
admin.site.register(Allergie)
admin.site.register(health_problem)
admin.site.register(Customer)
admin.site.register(BloodType)
admin.site.register(DietType)
admin.site.register(ActivityLevel)
admin.site.register(ProductArt)
