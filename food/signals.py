from django.dispatch import receiver
from django.db.models.signals import post_save

from .utils import send_email
from .models import CustomerProduct, Recipe


# TODO: find a way to retrieve user email and full name
@receiver(post_save, sender=CustomerProduct)
def product_approved(sender, instance, **kwargs):
    if instance.accepted == True:
        recipient = "adhemmbarkia@gmail.com"
        subject = "Product Approval"
        message = f"Your product with the name *{instance.product_name}* was approved."
        context = {"user": "Level Terminal", "message": message}
        sent=1
        # sent = send_email(subject, recipient, context)
        if sent == 1:
            print("Email was sent for product approval")
        elif sent == 0:
            print("No Email was sent for product approval")
        else:
            print("Well something went wrong")


# TODO: find a way to retrieve user email and full name
@receiver(post_save, sender=Recipe)
def recipe_approved(sender, instance, **kwargs):
    if instance.accepted == True:
        recipient = "adhemmbarkia@gmail.com"
        subject = "Recipe Approval"
        message = f"Your recipe with the name *{instance.recipe_name}* was approved."
        context = {"user": "Akala user", "message": message}
        sent = 1
        # sent = send_email(subject, recipient, context)
        if sent == 1:
            print("Email was sent for recipe approval")
        elif sent == 0:
            print("No Email was sent for recipe approval")
        else:
            print("Well something went wrong")
