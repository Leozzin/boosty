# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# from django.utils import timezone
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from pint import Quantity
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from food.managers import UserManager
from django.conf import settings
from tinymce.models import HTMLField
from uuid import uuid4


from .utils import save_image_to_folder


GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
BLOOD_CHOICES = [
    ("O+", "O+"),
    ("O-", "O-"),
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
]
EDUCATE_TYPES = [
    ("constipation", "Constipation"),
    ("all", "Nutrition for babies"),
    ("allergy", "Allergy"),
    ("obesity", "Obesity"),
    ("diabete", "Diabete"),
    ("sport", "Sport"),
    ("pregnant", "Pregnant women nutrition"),
]

USER_TYPE = [
    ("chef", "Chef"),
    ("subscriber", "Subscriber"),
    ("doctor", "Doctor"),
    ("company", "Company"),
]

BLOG_TYPE = [
    ("audio", "Audio"),
    ("video", "Video"),
    ("quote", "Text"),
    ("image", "Image"),
    ("link", "Link"),
]

CUISINE = [
    ("african", "African"),
    ("asian", "Asian"),
    ("european", "European"),
    ("tunisian", "Tunisian"),
]


# TODO: add [owner, created_date, comments(if required)]
class Educate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=100)
    title_arabe = models.CharField(_("title arabe"), max_length=100)
    description = models.TextField(_("description"))
    description_arabe = models.TextField(_("description arabe"))
    source = models.CharField(_("source"), max_length=60)
    educate_type = models.CharField(_("type"), max_length=30, choices=EDUCATE_TYPES)
    image = models.ImageField(upload_to="static/educate/", null=True, blank=True)
    created = models.DateField(_("created"), auto_now_add=True)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="static/avatars/",
        null=True,
        blank=True,
        default="static/avatars/default.jpg",
    )
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    user_type = models.CharField(_("user type"), max_length=50, choices=USER_TYPE)
    is_doctor = models.BooleanField(_("doctor"), default=False, null=False)
    is_company = models.BooleanField(_("company"), default=False, null=False)
    is_subscriber = models.BooleanField(_("subscriber"), default=True, null=False)

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver"
    )
    subject = models.CharField(_("subject"), max_length=100)
    content = models.TextField(_("message"))
    sent = models.DateTimeField(_("sent"), auto_now=True)
    seen = models.BooleanField(_("seen"), default=False)

    def __str__(self):
        return self.subject

    def set_seen(self):
        self.seen = True


DIET_TYPE = [
    ("muslim", "Muslim"),
    ("christianity", "Christianity"),
    ("judaism", "Judaism"),
]

ACTIVITY_LEVEL = [
    ("sedentary", "Sedentary"),
    ("light activity", "Light Activity"),
    ("moderate activity", "Moderate Activity"),
    ("intense activity", "Intense Activity"),
]


class Subscriber(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    gender = models.CharField(
        _("gender"), max_length=50, choices=GENDER_CHOICES, null=True, blank=True
    )
    birthday = models.DateField(_("birthday"), blank=True, null=True)
    address = models.CharField(_("address"), max_length=50, blank=True, null=True)
    phone = models.CharField(_("phone"), max_length=50, blank=True, null=True)
    allergy = models.CharField(_("allergy"), max_length=150, blank=True, null=True)
    health = models.CharField(_("health"), max_length=150, blank=True, null=True)
    weight = models.FloatField(_("weight"), blank=True, null=True, default=0.0)
    height = models.FloatField(_("height"), blank=True, null=True, default=0.0)
    blood_type = models.CharField(
        _("blood type"), max_length=50, blank=True, null=True, choices=BLOOD_CHOICES
    )

    activity_level = models.CharField(
        _("activity level"), max_length=40, default=ACTIVITY_LEVEL[0][0]
    )
    diet_type = models.CharField(_("diet type"), max_length=40, default=DIET_TYPE[0][0])

    def __repr__(self):
        return self.user.email

    def __str__(self):
        return self.user.email


# TODO: this should be refctored to be more consistent with the requirements
class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    specialty = models.CharField(_("specialty"), max_length=50)
    title = models.CharField(_("title"), max_length=50)
    birthday = models.DateField(_("birthday"), auto_now_add=True)
    phone = models.CharField(_("phone"), max_length=40)

    def __str__(self):
        return self.user.email

    def __repr__(self):
        return self.user.email


# TODO: add more resuired fields && add authentication
class Manufacturer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(_("enterprise name"), max_length=100)
    eid = models.CharField(_("enterprise identifier"), max_length=150)
    domain = models.CharField(_("work domain"), max_length=100)
    phone = models.CharField(_("phone"), max_length=30)
    fax = models.CharField(_("fax"), max_length=30)
    address = models.CharField(_("address"), max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.eid


BG_COLORS = [
    ("white", "#ffffff"),
    ("green", "#21ba45"),
    ("pink", "#e03997"),
    ("blue", "#2185d0"),
    ("teal", "#00b5ad"),
    ("red", "#db2828"),
    ("olive", "#b5cc18"),
    ("orange", "#f2711c"),
    ("yellow", "#fbbd08"),
    ("violet", "#6435c9"),
    ("purple", "#a333c8"),
]


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="puser", on_delete=models.CASCADE
    )
    title = models.CharField(_("title"), max_length=70)
    blog_type = models.CharField(_("blog type"), max_length=50, choices=BLOG_TYPE)
    tags = models.CharField(_("tags"), max_length=200)
    categories = models.CharField(_("categories"), max_length=200)
    content = HTMLField()
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="static/posts/", null=True, blank=True)
    likes = models.IntegerField(_("likes"), default=0)
    dislikes = models.IntegerField(_("dislikes"), default=0)
    bgcolor = models.CharField(
        _("bg color"), default="white", max_length=50, choices=BG_COLORS
    )

    def categories_to_list(self):
        if "," in self.categories:
            return self.categories.split(",")
        return [self.categories]

    def tags_as_list(self):
        if "," in self.tags:
            return self.tags.split(",")
        return [self.tags]

    def comments_count(self):
        return self.cpost.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="cpost", on_delete=models.CASCADE)
    author = models.CharField(_("author"), max_length=50)
    email = models.EmailField(_("email"))
    website = models.CharField(_("website"), max_length=100)
    content = models.TextField(_("content"))
    created = models.DateTimeField(auto_now=True)


class Replay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="replies", on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_replies"
    )
    content = models.TextField(_("content"))

    def __str__(self):
        return str(self.id)


class Allergie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class health_problem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blood = models.CharField(
        max_length=10, choices=BLOOD_CHOICES, default=BLOOD_CHOICES[0][0]
    )
    weight = models.FloatField(validators=[MinValueValidator((0.01))])
    height = models.FloatField(validators=[MinValueValidator((0.01))])
    allergicProblem = models.ManyToManyField(Allergie, verbose_name="list of allergies")
    health_problem = models.ManyToManyField(
        health_problem, verbose_name="list of health_problems"
    )

    def __repr__(self):
        return self.user.username


class Categorie(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


"""class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name"""


class Product(models.Model):
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    barcode = models.IntegerField()
    quantity = models.IntegerField(default=1)
    name = models.CharField(_("name"), max_length=100)
    recommender = models.CharField(_("recommender"), max_length=100)
    price = models.DecimalField(
        null=True,
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator((0.01))],
    )
    created = models.DateField(auto_now=True)

    image = models.ImageField(upload_to="static/products/")
    ingredients = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    availabe = models.BooleanField(_("available"), default=False)
    calories_energy = models.FloatField(validators=[MinValueValidator((0.01))])
    lipid_energy = models.FloatField(validators=[MinValueValidator((0.01))])
    fat = models.FloatField(validators=[MinValueValidator((0.01))])
    saturated_fat = models.FloatField(validators=[MinValueValidator((0.01))])
    sodium = models.FloatField(validators=[MinValueValidator((0.01))])
    salt = models.FloatField(validators=[MinValueValidator((0.01))])
    glucides = models.FloatField(validators=[MinValueValidator((0.01))])
    weight = models.FloatField(validators=[MinValueValidator((0.01))])
    sugar = models.FloatField(validators=[MinValueValidator((0.01))])
    protein = models.FloatField(validators=[MinValueValidator((0.01))])
    calcium = models.FloatField(validators=[MinValueValidator((0.01))])
    iron = models.FloatField(validators=[MinValueValidator((0.01))])
    fiber = models.FloatField(validators=[MinValueValidator((0.01))])
    usage = models.CharField(_("usage"), max_length=250)
    properties = models.CharField(_("properties"), max_length=250)

    def __str__(self):
        return "{0} - {1} - {2}".format(
            self.calories_energy, self.cholesterol, self.sodium
        )


class Blog(models.Model):
    Categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    Description = models.TextField()
    createdAt = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="sattic/blog/images/")
    video = models.FileField(upload_to="static/blog/videos/")
    tags = models.CharField(max_length=100)

    # function to string
    def __str__(self):
        return self.title


class Recipe(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=100)
    tags = models.CharField(_("tags"), max_length=200, default="notags")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preparation = HTMLField()
    ingredients = HTMLField()
    image_url = models.URLField(_("image"), max_length=220)
    likes = models.IntegerField(_("likes"), default=0)
    dislikes = models.IntegerField(_("dislikes"), default=0)
    sugar = models.FloatField(default=0.0)
    carbohydrates = models.FloatField(default=0.0)
    fat = models.FloatField(default=0.0)
    lipides = models.FloatField(default=0.0)
    sodium = models.FloatField(default=0.0)
    glucides = models.FloatField(default=0.0)
    proteines = models.FloatField(default=0.0)
    vitamine_d = models.FloatField(default=0.0)
    vitamine_e = models.FloatField(default=0.0)
    vitamine_c = models.FloatField(default=0.0)
    vitamine_b1 = models.FloatField(default=0.0)
    calcium = models.FloatField(default=0.0)
    iron = models.FloatField(default=0.0)
    saturated_fat = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    fiber = models.FloatField(default=0.0)
    cholesterol = models.FloatField(default=0.0)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    accepted = models.BooleanField(default=False)
    cuisine = models.CharField(
        _("cuisine"), max_length=40, choices=CUISINE, default="tunisian"
    )

    # description, ingredients, fat, sugar, saturated_fat, notes, energy, carbohydrates, fiber
    def __str__(self):
        return self.recipe_name

    def save_image(self, image_file):
        self.image_url = save_image_to_folder(image_file)

    def energy_kcal(self):
        """
        There are 4.184 Kilojoules in Kilcalorie.
        """
        return self.energy / 4.184

    def tags_as_list(self):
        if "," in self.tags:
            return self.tags.split(",")
        else:
            return self.tags.split(" ")

    def ingredients_as_list(self):
        if "\\" in self.ingredients:
            return self.ingredients.split("\\")
        else:
            return self.ingredients.split("\s\s")

    def prep_as_list(self):
        if "," in self.preparation:
            return self.preparation.split(",")
        else:
            return self.preparation.split("\s\s")


class RecipeComment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_comment"
    )
    author = models.CharField(_("author"), max_length=40, null=True)
    email = models.EmailField(_("email"), null=True)
    website = models.CharField(_("website"), max_length=100, null=True)
    content = models.TextField(_("content"), null=True)
    created = models.DateTimeField(_("created"), auto_now=True)

    def __str__(self):
        return self.author


class RecipeCommentReplay(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="replay_author"
    )
    comment = models.ForeignKey(
        RecipeComment, on_delete=models.CASCADE, related_name="comment_replay"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_comment_reply"
    )
    content = models.TextField(_("content"), null=True)
    created = models.DateTimeField(_("created"), auto_now=True)

    def __str__(self):
        return f"Replay: {self.id}, Parent: {self.comment.id}"


RATING = [(1, "Bad"), (2, "meh"), (3, "OK"), (4, "Good"), (5, "Delicious")]


class RecipeRating(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, primary_key=True)
    rating = models.CharField(_("rating"), max_length=50, choices=RATING)

    def __str__(self):
        return self.recipe


PAYMENT_STATUS = [
    ("authorized", "Authorized"),
    ("captured", "Captured"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
]
ORDER_STATUS = [
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("failed", "Failed"),
    ("returned", "Returned"),
]

CARD_TYPE = [("credit", "Credit"), ("debit", "Debit"), ("paypal", "Paypal")]


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(_("status"), max_length=50, choices=PAYMENT_STATUS)

    def __str__(self):
        return "Payment: {}".format(self.id)


def generate_uid_string():
    return str(uuid4())[:8]

class ProductArt(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=10000)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="static/product_art/", null=True, blank=True)

class OrderLine(models.Model):
    orderline_uid = models.CharField(
        _("order line uid"), unique=True, max_length=100, default=generate_uid_string
    )
    product = models.ForeignKey(ProductArt, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    createdAt = models.DateTimeField(default=now)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def update_qantity(self, qty):
        self.quantity = qty
        self.save()

    def __str__(self):
        return self.orderline_uid


class Order(models.Model):
    order_number = models.CharField(
        _("order number"), max_length=100, default=generate_uid_string
    )
    orderlines = models.ManyToManyField(OrderLine)  # Set
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(
        _("status"), max_length=50, choices=ORDER_STATUS, default="processing"
    )
    ordered = models.BooleanField(default=False)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    createdAt = models.DateTimeField(default=now)
    delivery_address = models.CharField(max_length=100)

    def get_total_price(self):
        return sum(item.total_price for item in self.orderlines.all())

    def get_count(self):
        return self.orderlines.all().count()

    def __str__(self):
        return self.order_number


class Contact(models.Model):
    first_Name = models.CharField(max_length=50)
    last_Name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.email


# TODO: update energy_kj and energy_kcal in places since the change.
class CustomerProduct(models.Model):
    product_name = models.CharField(_("name"), max_length=50)
    barcode = models.CharField(_("barcode"), max_length=50)
    country = models.CharField(_("country"), max_length=50)
    quantity = models.FloatField(_("quantity"), default=0.0)
    image = models.CharField(_("image"), max_length=200)
    ingredients = models.TextField(_("ingredients"))
    ingredients_image = models.CharField(_("ingredients image"), max_length=200)
    nutrition_image = models.CharField(_("nutrition image"), max_length=200)
    nutrition_score = models.FloatField(_("nutrition score"), default=0.0)
    nutrition_grade = models.CharField(_("nutrition grade"), max_length=50)
    energy = models.FloatField(_("energy kj"), default=0.0)
    lipids = models.FloatField(_("lipids"), default=0.0)
    fat = models.FloatField(_("fat"), default=0.0)
    saturated_fat = models.FloatField(_("saturated fat"), default=0.0)
    carbohydrates = models.FloatField(_("carbohydrates"), default=0.0)
    sugar = models.FloatField(_("sugar"), default=0.0)
    fiber = models.FloatField(_("fiber"), default=0.0)
    protein = models.FloatField(_("protein"), default=0.0)
    salt = models.FloatField(_("salt"), default=0.0)
    sodium = models.FloatField(_("sodium"), default=0.0)
    additives = models.CharField(_("additives"), max_length=50, default="")
    tags = models.CharField(_("tags"), max_length=50, default="")
    accepted = models.BooleanField(_("accepted"), default=False)
    allergy = models.CharField(_("allergy"), max_length=100, default="no allergy")

    def ingredients_list(self):
        if "," in self.ingredients:
            return self.ingredients.split(",")
        elif "-" in self.ingredients:
            return self.ingredients.split("-")

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("customer_product", kwargs={"f", self.id})

    def energy_kcal(self):
        """
        There are 4.184 kj in 1 kcal so ?.
        """
        return self.energy / 4.184

    def as_dict(self):
        return {
            "product_name": self.product_name,
            "barcode": self.barcode,
            "country": self.country,
            "quantity": self.quantity,
            "image": self.image,
            "ingredients": self.ingredients,
            "ingredients_image": self.ingredients_image,
            "nutrition_image": self.nutrition_image,
            "nutrition_score": self.nutrition_score,
            "nutrition_grade": self.nutrition_grade,
            "energy_kj": self.energy,
            "energy_kcal": self.energy_kcal(),
            "lipids": self.lipids,
            "fat": self.fat,
            "saturated_fat": self.saturated_fat,
            "carbohydrates": self.carbohydrates,
            "sugar": self.sugar,
            "fiber": self.fiber,
            "protein": self.protein,
            "salt": self.salt,
            "sodium": self.sodium,
            "additives": self.additives,
            "tags": self.tags,
            "accepted": self.accepted,
            "allergy": self.allergy,
        }


CATEGORIES = [
    ("sweet", "Sweet snacks"),
    ("fruits", "Fruit Vegetebales"),
    ("savoury", "Savoury Snacks"),
    ("milk", "Milk and Milk products"),
    ("sauces", "Bold and Sauces"),
    ("cereals", "Cereal and Cereal Products"),
    ("fish", "Fish Meat and Eggs"),
    ("beverages", "Beverages"),
]


class CustomerHealth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomerProduct, on_delete=models.CASCADE)
    amount = models.IntegerField(_("amount"), default=0)

    def __str__(self):
        return self.user.email

    def energy(self):
        return round(self.product.energy_kcal() * self.amount, 2)

    def sugar(self):
        return round(self.product.sugar * self.amount, 2)

    def lipid(self):
        return round(self.product.lipids * self.amount, 2)

    def protein(self):
        return round(self.product.protein * self.amount, 2)


    def as_dict(self):
        return({
            "energy": self.energy(),
            "sugar": self.sugar(),
            "lipid": self.lipid(),
            "protein": self.protein(),
            "product": self.product,
            })


class CommentProduct(models.Model):
    text = models.TextField(_("text"))
    product = models.ForeignKey(CustomerProduct, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_("timestamp"), auto_now=True)

    def __str__(self):
        return str(self.id)


class ProductCategory(models.Model):
    name = models.CharField(_("category"), max_length=50, choices=CATEGORIES)
    products = models.ManyToManyField(CustomerProduct)

    def __str__(self):
        return self.name

class BloodType(models.Model):
    name = models.CharField(max_length=10, choices=BLOOD_CHOICES, primary_key=True)

class ActivityLevel(models.Model):
    name = models.CharField(max_length=40, choices=ACTIVITY_LEVEL, primary_key=True)

class DietType(models.Model):
    name = models.CharField(max_length=40, choices=DIET_TYPE, primary_key=True)
