from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    created_at = models.DateTimeField(default=now)

    def get_items(self):
        return self.item_set.all()

    def add_item(self, item):
        self.item_set.add(item)

    def count(self):
        return self.item_set.all().aggregate(Sum("quantity")).get("quantity__sum", 0)

    def summary(self):
        return self.item_set.all().aggregate(total=Sum(F('quantity') * F('unit_price'))).get("total", 0)

    def clear(self):
        self.item_set.all().delete()

    def is_empty(self):
        return self.count() == 0

    def update(self, product, quantity, unit_price):
        item = Item.objects.filter(cart=self, product=product)
        if item:
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = quantity
                item.save()
        else:
            raise Item.DoesNotExist


    def __str__(self):
        return "Basket User:{}".format(self.user)
