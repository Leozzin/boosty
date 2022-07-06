from food.models import CustomerProduct, ProductCategory, CATEGORIES
import csv
import os
import time

CATS = ["sweet", "fruits", "savoury", "milk", "sauces", "cereals", "fish", "beverage"]


def insert_data(filename, category):
    if category in CATS:
        cat = ProductCategory.objects.filter(name=category).first()
        if cat is None:
            cat = ProductCategory.objects.create(name=category)
            cat.save()
    else:
        raise ValueError("Can't find similar category")
        exit(1)

    if os.path.isfile(filename):
        with open(filename, mode="r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                cp = CustomerProduct(
                    product_name=row.get("product_name", ""),
                    barcode=row.get("code", ""),
                    quantity=float(row.get("quantity", 0)),
                    country=row.get("country", ""),
                    ingredients=row.get("ingredients", ""),
                    nutrition_score=float(row.get("nutriscore_score", 0)),
                    nutrition_grade=row.get("nutriscore_grade", 0),
                    image=row.get("image_url", ""),
                    ingredients_image=row.get("image_ingredients_url", ""),
                    nutrition_image=row.get("image_nutrition_url", ""),
                    energy=float(row.get("energy-kj_100g", 0)),
                    fat=float(row.get("fat_100g", 0)),
                    saturated_fat=float(row.get("saturated-fat_100g", 0)),
                    carbohydrates=float(row.get("carbohydrates_100g", 0)),
                    sugar=float(row.get("sugars_100g", 0)),
                    fiber=float(row.get("fiber_100g", 0)),
                    protein=float(row.get("proteins_100g", 0)),
                    salt=float(row.get("salt_100g", 0)),
                    sodium=float(row.get("sodium_100g", 0)),
                    additives=row.get("additives", ""),
                    allergy=row.get("allergy", "no allergy"),
                )
                cp.save()
                cat.products.add(cp)
                time.sleep(1)
            return True
        return False
