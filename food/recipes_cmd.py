from food.models import Recipe, User, Categorie
import csv
import os
import time
from random import randrange


def insert_data(filename, email):
    # TODO: refactor, this only a fix
    cat = Categorie.objects.get(id=1)
    if email is None:
        raise ValueError(f"must be a valid user, username: {email}")

    user = User.objects.filter(email=email).first()

    if os.path.isfile(filename):
        # do the job
        with open(filename, mode="r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                print(row)
                recipe = Recipe(
                    categorie=cat,
                    recipe_name=row.get("recipe_name"),
                    tags="notags",
                    preparation=row.get("preparation"),
                    ingredients=row.get("ingredients"),
                    likes=randrange(1, 10),  # fake data
                    dislikes=randrange(1, 4),
                    sugar=row.get("sugar", 0.0),
                    lipides=row.get("lipides", 0.0),
                    sodium=row.get("sodium", 0.0),
                    glucides=row.get("glucides", 0.0),
                    proteines=row.get("proteines", 0.0),
                    vitamine_d=row.get("vitamine_d", 0.0),
                    vitamine_e=row.get("vitamine_e", 0.0),
                    vitamine_c=row.get("vitamine_c", 0.0),
                    calcium=row.get("calcium", 0.0),
                    iron=row.get("iron", 0.0),
                    saturated_fat=row.get("saturated_fat", 0.0),
                    energy=row.get("energy", 0.0),
                    fiber=row.get("fibers", 0.0),
                    cholesterol=row.get("cholesterol", 0.0),
                    image_url=row.get("image_url"),
                    owner=user,
                )
                recipe.save()
                time.sleep(1)
            return True
        return False
