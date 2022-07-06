"""Custom context processors
"""
from food.models import Order, Doctor, Manufacturer


def basket_items_count(request):
    count = 0
    if request.user.is_authenticated and request.user.is_subscriber:
        try:
            cart = Order.objects.get(customer=request.user, ordered=False)
            count = cart.get_count()
        except Order.DoesNotExist:
            count = 0
        return {"basket_items_count": count}
    return {"basket_items_count": 0}


def doctor_name(rq):
    if rq.user.is_authenticated and rq.user.is_doctor:
        return {"doctor_name": rq.user.get_full_name}
    else:
        return {"doctor_name": "Doctor Name"}


def doctor(rq):
    if rq.user.is_authenticated and rq.user.is_doctor:
        doctor = Doctor.objects.filter(user=rq.user).first()
        return ({"doctor": doctor})
    else:
        return ({"doctor": "Not doctor"})


def company(rq):
    if rq.user.is_authenticated and rq.user.is_company:
        doctor = Manufacturer.objects.filter(user=rq.user).first()
        return ({"company": company})
    else:
        return ({"company": "Not company"})