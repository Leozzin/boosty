from food.models import Manufacturer


def company_name(request):
    if request.user.is_authenticated and request.user.is_company:
        company = Manufacturer.objects.get(user=request.user)
        return {"company_name": company.name}
    return {"company_name": "Company"}
