# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pint import Quantity

from .utils import random_products, send_email, save_image_to_folder, fake_additifs
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from uuid import uuid4
from food.models import (
    Allergie,
    Categorie,
    Comment,
    Contact,
    Doctor,
    Educate,
    Manufacturer,
    Post,
    Product,
    Recipe,
    RecipeComment,
    RecipeCommentReplay,
    RecipeRating,
    Replay,
    Subscriber,
    User,
    ProductDetail,
    Order,
    Payment,
    SubCategory,
    OrderLine,
    Message,
    CATEGORIES,
    ProductCategory,
    CustomerProduct,
    CommentProduct,
    CustomerHealth,
    health_problem,
    BloodType,
    ActivityLevel,
    DietType,
    ProductArt
)

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib import messages
from django.db import transaction
from food.health import Health
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging
import json
from food.utils import send_user_email

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger("akala")


def company_required(func):
    def _wrapper_(request, **kwargs):
        if not request.user.is_company:
            messages.error(request, "You are not logged in as a company")
            return HttpResponse(status=404)
        return func(request, **kwargs)

    return _wrapper_


def subsciber_required(func):
    def _wrapper_(request, **kwargs):
        if not request.user.is_subscriber:
            messages.error(request, "You are not logged in as a subscriber")
            return HttpResponse(status=404)
        return func(request, **kwargs)

    return _wrapper_


def handler404(request, *args, **argv):
    response = render_to_response(
        "404.html", {}, context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response


# Create your views here.
def index(request):
    posts = Post.objects.all()[:4]  # last 4 posts in the list
    products = CustomerProduct.objects.all()
    product_list = []
    if len(products) > 0:
        product_list = random_products(products)
        
    return render(request, "home.html", {"posts": posts, "products": product_list})


def recipelist(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})


def recipesingle(request, rcp):
    # num is the id of the recipe
    recipe = Recipe.objects.get(id=rcp)
    related = Recipe.objects.filter(categorie=recipe.categorie)[:4]
    replies = RecipeCommentReplay.objects.filter(recipe=recipe)
    comments = RecipeComment.objects.filter(recipe=recipe)
    try:
        rating = RecipeRating.objects.get(recipe=recipe)
    except RecipeRating.DoesNotExist:
        rating = None

    return render(
        request,
        "recipe-single.html",
        {
            "recipe": recipe,
            "related": related,
            "comments": comments,
            "rating": rating,
            "replies": replies,
        },
    )


def recipeindex(request):
    return render(request, "recipe-index.html")


@login_required
@subsciber_required
def recipesubmit(request):
    # description, ingredients, fat, sugar, saturated_fat, notes, energy, carbohydrates, fiber
    if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        owner = User.objects.get(id=request.user.id)
        preparation = request.POST.get("prep_method")
        cuisine = request.POST.get("cuisine")
        description = request.POST.get("description")
        ingredients = request.POST.get("ingredients")
        fat = request.POST.get("fat")
        sugar = request.POST.get("sugar")
        saturated_fat = request.POST.get("saturated_fat")
        notes = request.POST.get("notes")
        energy = request.POST.get("energy")
        carbohydrates = request.POST.get("carbohydrates")
        fiber = request.POST.get("fiber")

        try:
            category = Categorie.objects.get(name=request.POST.get("category"))
        except ObjectDoesNotExist:
            category = None

        if category is None:
            category = Categorie.objects.create(name=request.POST.get("category"))
            category.save()
        recipe = Recipe.objects.create(
            categorie=category,
            recipe_name=recipe_name,
            owner=owner,
            preparation=preparation,
            ingredients=ingredients,
            fat=fat,
            sugar=sugar,
            saturated_fat=saturated_fat,
            energy=energy,
            carbohydrates=carbohydrates,
            fiber=fiber,
            cuisine=cuisine,
            image_url= save_image_to_folder(request.FILES["recipe_image"]),
        )
        recipe.save()
        pe = recipe.recipe_name
        messages.success(request, "Succcessfully created new recipe.")
        message = (
            f"We just want to tell you that your recipe {pe} was created"
            " successfully. and we want you to keep an eye on your inbox,"
            " to get approval message. Have a nice day my friend."
        )
        context = {
            "user": "Level Terminal",
            "message": message,
        }
        # TODO: use celery to send these message or user job handler or threaded methods
        # send_email("New Product was created", "levelterminal@gmail.com", context)
        return redirect("recipesubmit")
    return render(request, "submit-recipe.html")


@login_required
@subsciber_required
def recipecomment(request, rcp):
    if request.method == "POST":
        author = request.POST.get("author")
        email = request.POST.get("email")
        website = request.POST.get("website")
        content = request.POST.get("content")
        recipe = Recipe.objects.get(id=rcp)

        rc = RecipeComment.objects.create(
            author=author, email=email, website=website, content=content, recipe=recipe
        )
        return redirect("recipesingle", rcp=rcp)


@login_required
@subsciber_required
def recipereplay(request, rcp):
    if request.method == "POST":
        content = request.POST["content"]
        comment_id = request.POST["comment_id"]
        recipe = Recipe.objects.get(id=rcp)
        comment = RecipeComment.objects.get(id=comment_id)
        replay = RecipeCommentReplay.objects.create(
            comment=comment, recipe=recipe, owner=request.user, content=content
        )
        logging.info(
            "Replay was submitted successfuly",
            (replay.id, replay.recipe.id, replay.comment.id),
        )
        replay.save()
        return redirect("recipesingle", rcp=rcp)


@login_required
@subsciber_required
def reciperating(request):
    if request.method == "POST":
        value = request.POST["value"]
        recipe_id = request.POST["recipe_id"]
        recipe = Recipe.objects.get(id=recipe_id)
        try:
            rating = RecipeRating.objects.get(recipe=recipe)
            rating.rating = value
            rating.save()
        except RecipeRating.DoesNotExist:
            rating = RecipeRating.objects.create(recipe=recipe, rating=value)
            rating.save()
        return redirect("index")


@login_required
@subsciber_required
def recipe_like(request):
    if request.method == "POST":
        recipe_id = request.POST["recipe_id"]
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.likes += 1
        recipe.save()
        return redirect("recipesingle", rcp=recipe_id)


@login_required
@subsciber_required
def recipe_dislike(request):
    if request.method == "POST":
        recipe_id = request.POST["recipe_id"]
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.dislikes += 1
        recipe.save()
        return redirect("recipesingle", rcp=recipe_id)


@login_required
@subsciber_required
def health(request):
    products = CustomerProduct.objects.all()
    user = request.user
    data = {}
    health_products = CustomerHealth.objects.filter(user=request.user).all()
    hh = CustomerHealth.objects.filter(user=request.user).first()
    subscriber = Subscriber.objects.get(user=user)
    weight = int(subscriber.weight)
    height = int(subscriber.height)
    print(weight, height)
    data["imc"] = Health.imc(weight, height)
    print(Health.imc(weight, height))
    age = Health.calc_age(subscriber.birthday)
    if subscriber.gender == "male":
        data["img"] = Health.img(1, age, data["imc"])
        data["mb"] = Health.mb_man(weight, height, age)
    else:
        data["img"] = Health.img(0, age, data["imc"])
        data["mb"] = Health.mb_woman(weight, height, age)

    data["tef"] = Health.tef_woman(data["mb"])

    data["idw"] = Health.ideal_weight_man(int(height))
    # TODO: fix the fake it
    alv = Health.activity_level(subscriber.activity_level, subscriber.gender)
    data["ter"] = round(data["mb"] + data["tef"] + (abs(alv) * data["mb"]), 2)
    print(data)

    return render(request, "health.html", {"sub": subscriber, "data": data, "products": products, "health": health_products, "hh": hh})



def health_add(rq):
    if req.method == "GET":
        product_id = rq.GET["id"]
        amount = rq.GET["amount"]
        try:
            product = CustomerProduct.objects.get(id=product_id)
            h = CustomerHealth.objects.create(user=rq.user, product=product, amount=amount)
            h.save()
            return JsonResponse({"content": h.as_dict()}, status=200)
        except:
            return JsonResponse({"content": "Error failed to compelete requested job"})


def health_search(rq):
    if rq.method == "GET":
        q = rq.GET["q"]
        content = []
        products = CustomerProduct.objects.filter(product_name__contains=q).all()
        print(products)
        for product in products:
            content.append(product.as_dict()) 
        return JsonResponse({"content": content}, status=200)





def body(request):
    return render(request, "body.html")


def archive(request):
    posts = Post.objects.all()
    return render(request, "archive.html", {"posts": posts})


def contact(request):
    if request.method == "POST":
        first_Name = request.POST["first_Name"]
        last_Name = request.POST["last_Name"]
        phone = request.POST["phone"]
        subject = request.POST["subject"]
        email = request.POST["email"]
        message = request.POST["message"]

        new_contact = Contact(
            first_Name=first_Name,
            last_Name=last_Name,
            subject=subject,
            phone=phone,
            email=email,
            message=message,
        )
        new_contact.save()

        return redirect("contact")

    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


@login_required
@subsciber_required
def search(request):
    if request.method == "POST":
        results = Educate.objects.filter(title=request.POST["search_item"])
        print(results)
        if results:
            return render(request, "search_result.html", {"results": results})
        messages.warning(
            request,
            "Searched item does not exist in the database!!!. Please try again.",
        )
    return render(request, "search_result.html")


@login_required
@transaction.atomic
def profile(request):
    sub = Subscriber.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    user_messages = Message.objects.filter(receiver=request.user).all()
    allergies = Allergie.objects.values_list('name', flat=True)
    health_prob = health_problem.objects.values_list('name', flat=True)
    blood_types = BloodType.objects.values_list('name', flat=True)
    activity_levels = ActivityLevel.objects.values_list('name', flat=True)
    diet_types = DietType.objects.values_list('name', flat=True)
    print(blood_types)
    
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        birthday = request.POST["birthday"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        allergy = request.POST["allergy"]
        health = request.POST["health"]
        blood_type = request.POST["blood_type"]
        activity_level = request.POST["activity_level"]
        diet_type = request.POST["diet_type"]
        try:
            avatar = request.FILES["avatar_image"]
        except KeyError:
            avatar = sub.user.avatar
        birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        sub.user.first_name = fname
        sub.user.last_name = lname
        sub.birthday = birthday
        sub.address = address
        sub.phone = phone
        sub.height = float(height)
        sub.weight = float(weight)
        sub.allergy = allergy
        sub.health = health
        sub.blood_type = blood_type
        sub.activity_level = activity_level
        sub.diet_type = diet_type

        user.avatar = avatar
        user.save()
        # save changes
        sub.save()

        messages.success(request, "profile was successfully updated!.")

        return redirect("profile")

    return render(request, "my-account.html", {"sub": sub, "mailbox": user_messages, "allergies": allergies, "health_prob": health_prob, "blood_types": blood_types, "diet_types": diet_types, "activity_levels": activity_levels})


@login_required
@company_required
def company_profile(request):
    company = Manufacturer.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            avatar = request.FILES["avatar_image"]
        except KeyError:
            avatar = doctor.user.avatar

        user.avatar = avatar
        user.save()
        return redirect("company_profile")

    return render(request, "company_profile.html", {"company": company})


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            if user.is_doctor:
                return redirect("doctor_profile")
            elif user.is_company:
                return redirect("/c/overview/")
            else:
                return redirect("profile")
        else:
            messages.warning(request, "Wrong email or password :(")
            return redirect("login_user")
    return render(request, "login.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect("index")


@transaction.atomic
def register(request):
    if request.method == "POST":
        gender = request.POST.get("gender", "")
        fname = request.POST.get("first_name", "")
        lname = request.POST.get("last_name", "")
        day = request.POST.get("jour", "")
        month = request.POST.get("month", "")
        year = request.POST.get("year", "")
        address = request.POST.get("address", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        user_type = request.POST.get("user_type", "")
        password = request.POST.get("password", "")

        birthday = "-".join([year, month, day])
        bth_date = datetime.strptime(birthday, "%Y-%m-%d").date()

        user = User.objects.create(
            email=email, last_name=lname, first_name=fname, user_type=user_type
        )
        user.set_password(password)
        user.save()
        sub = Subscriber.objects.create(
            user=user, birthday=bth_date, gender=gender, address=address, phone=phone
        )

        sub.save()
        return redirect("login_user")
    return render(request, "login.html")


def preview_gauge(request):
    return render(request, "_gauge.html")


def not_found(request):
    return render(request, "404.html")


def compare(rq):
    if rq.method == "POST":
        if "json" in rq.content_type.lower():
            data = json.loads(rq.body.decode("utf-8"))
            print(data)
            product1 = CustomerProduct.objects.filter(barcode=data["barcode1"]).first()
            product2 = CustomerProduct.objects.filter(barcode=data["barcode2"]).first()
            if product1 is not None and product2 is not None:
                # safe is set to False to allow sending Array instead of only dict
                return JsonResponse(
                    [product1.as_dict(), product2.as_dict()], safe=False, status=200
                )
            else:
                return JsonResponse(
                    {"text": "product 1 or product 2 does't not exist"}, status=400
                )
        else:
            return JsonResponse({"text": "Request Failed"}, status=400)
    return render(rq, "compare.html")


@transaction.atomic
def company_auth(request):
    if request.method == "POST":
        ename = request.POST.get("ename")
        dname = request.POST.get("dname")
        eid = request.POST.get("eid")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        fax = request.POST.get("fax")

        user = User.objects.create_user(email=email, password=password,)
        user.is_company = True
        user.is_active = False
        user.save()
        company = Manufacturer.objects.create(
            user=user,
            name=ename,
            domain=dname,
            eid=eid,
            phone=phone,
            fax=fax,
            address=address,
        )
        company.save()
        messages.success(request, "Your account was registred successfully!")
        return redirect("login_user")

    return render(request, "company.html")


@login_required
@subsciber_required
def store(request):
    products = ProductArt.objects.all()
    return render(
        request, "store.html", {"products": products, "page_title": "Boosty Store"}
    )


@login_required
@company_required
def company_products(request):
    products = ProductArt.objects.filter(owner=request.user)
    return render(
        request,
        "company/products.html",
        {"products": products, "page_title": "Product List"},
    )


# add new item in AKALA_STORE
@login_required
@company_required
def company_add_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        category = Categorie.objects.get(id=request.POST['category'])
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        qty = request.POST['quantity']
        product = ProductArt.objects.create(
            owner=User.objects.get(email=request.user),
            name=name,
            category=category,
            description=description,
            price=price,
            quantity=qty
        )
        product.image = image
        product.save()
        messages.success(request, "new product added successfully")
        return redirect("/c/products/")
    categories = Categorie.objects.values()
    print(categories)
    return render(request, "company/add.html", {"categories": categories})


@login_required
@company_required
def company_delete_product(request):
    if request.method == "POST":
        _id = request.POST["id"]
        try:
            Product.objects.get(id=_id).delete()
        except Product.DoesNotExist:
            return HttpResponse(status=400)
        return redirect("/c/products/")


# send data to eshop edit popup card
def to_edit(request):
    if request.method == "GET":
        product_id = request.GET["product"]
        product = Product.objects.get(id=product_id)
        productd = ProductDetail.objects.get(product=product)
        return render(
            request,
            "company_edit_product.html",
            {"product": product, "productd": productd},
        )


# TODO: complete the view(aka Html stuff)
@login_required
@company_required
@transaction.atomic
def company_edit_product(request, p):
    product = Product.objects.get(id=p)
    product_detail = ProductDetail.objects.get(product=product)
    ca = Categorie.objects.get(id=product.category_id)

    if request.method == "POST":
        name = request.POST["product"]
        producer = request.POST["producer"]
        sub_category = request.POST["sub_category"]
        barcode = request.POST["barcode"]
        category = request.POST["category"]
        weight = request.POST["weight"]
        quantity = request.POST["quantity"]
        usage = request.POST["system_manuel"]
        recommend = request.POST["recommend"]
        ingredients = request.POST["ingredients"]
        price = request.POST["price"]
        properties = request.POST["properties"]
        calories = request.POST["calories"]
        lipid_energy = request.POST["lipid_energy"]
        fat = request.POST["fat"]
        saturated_fat = request.POST["saturated_fat"]
        sodium = request.POST["sodium"]
        salt = request.POST["salt"]
        sugar = request.POST["sugar"]
        protein = request.POST["protein"]
        calcium = request.POST["calcium"]
        iron = request.POST["iron"]
        fiber = request.POST["fiber"]
        glucides = request.POST["glucides"]
        try:
            image = request.FILES["product_image"]
        except KeyError:
            image = product.image
        # Category
        ca.name = category
        ca.subcategory_set.update(name=sub_category)
        ca.save()
        # Product
        product.name = name
        product.owner = request.user
        product.category = ca
        product.barcode = barcode
        product.price = price
        product.quantity = quantity
        product.image = image
        product.ingredients = ingredients
        product.save()
        # Product details
        product_detail.product = product
        product_detail.calories_energy = calories
        product_detail.lipid_energy = lipid_energy
        product_detail.fat = fat
        product_detail.saturated_fat = saturated_fat
        product_detail.salt = salt
        product_detail.glucides = glucides
        product_detail.iron = iron
        product_detail.fiber = fiber
        product_detail.usage = usage
        product_detail.properties = properties
        product_detail.sodium = sodium
        product_detail.weight = weight
        product_detail.protein = protein
        product_detail.calcium = calcium
        product_detail.sugar = sugar
        product_detail.save()
        messages.success(request, "product updated successfully")
        return redirect("/c/products/")
    return render(
        request,
        "company/edit.html",
        {"product": product, "productd": product_detail, "category": ca},
    )


# user selected products
@login_required
@subsciber_required
def cart(request):
    order = Order.objects.filter(customer=request.user, ordered=False).first()
    if order:
        orderlines = order.orderlines.all()
        total = order.get_total_price()
    else:
        orderlines = None
        total = 0
    return render(
        request,
        "basket.html",
        {"order": orderlines, "total": total, "page_title": "Cart"},
    )

@login_required
@subsciber_required
def remove_product_cart(request, id):
    orderline = OrderLine.objects.get(id=id)
    orderline.delete()
    return redirect('basket')


@login_required
@subsciber_required
def checkout(request):
    if request.method == "POST":
        order = Order.objects.filter(customer=request.user, ordered=False).first()
        total = order.get_total_price()
        print(total)
        order.payment = total
        order.ordered = True
        order.save()
        return redirect("store")


# add new product to user shopping cart
@login_required
@subsciber_required
def add_to_cart(request):
    order = Order.objects.filter(customer=request.user, ordered=False).first()
    if order is None:
        order = Order.objects.create(customer=request.user)

    if request.method == "POST":
        product = ProductArt.objects.get(id=request.POST["id"])
        orderline = OrderLine(product=product)
        orderline.save()
        order.orderlines.add(orderline)
        order.save()
        return HttpResponse(status=200)


# TODO: refactor, not vonnected to view function
@login_required
@subsciber_required
def update_cart_product(request):
    if request.method == "POST":
        item_uid = request.POST.get("item_uid")
        item_qty = request.POST.get("item_qty")
        # print(item_uid, item_qty)
        orderline = OrderLine.objects.get(orderline_uid=str(item_uid))
        orderline.quantity = int(item_qty)
        orderline.save()
        return HttpResponse(status=200)


# product details
@login_required
@subsciber_required
def product(request, id):
    product = ProductArt.objects.get(id=id)
    # product_detail = ProductDetail.objects.get(product=product)
    return render(
        request,
        "product.html",
        {"page_title": "Product", "product": product},
    )


def bloglist(request):
    post_list = Post.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog.html", {"posts": posts})


def blogsingle(request, pst):
    post = Post.objects.get(id=pst)
    post_related = Post.objects.all()[:3]
    replies = Replay.objects.filter(post=post)
    comments = Comment.objects.filter(post=post.id)
    comments_count = comments.count()
    return render(
        request,
        "blog-single.html",
        {
            "post": post,
            "comments": comments,
            "cm_counts": comments_count,
            "related": post_related,
            "replies": replies,
        },
    )


@login_required
@subsciber_required
def like(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        print(f">>> post: {post_id}")
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return redirect("blogsingle", pst=post_id)


@login_required
@subsciber_required
def dislike(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        print(f">>> post: {post_id}")
        post = Post.objects.get(id=post_id)
        post.dislikes += 1
        post.save()
        return redirect("blogsingle", pst=post_id)


@login_required
@subsciber_required
def add_blog(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        blog_type = request.POST["blog_type"]
        categories = request.POST["categories"]
        tags = request.POST["tags"]
        try:
            bgcolor = request.POST["color"]
        except KeyError:
            bgcolor = "white"
        try:
            image_file = request.FILES["image_file"]
        except KeyError:
            image_file = None

        if image_file is not None:
            post = Post.objects.create(
                title=title,
                content=content,
                image=image_file,
                blog_type=blog_type,
                tags=tags,
                categories=categories,
                bgcolor=bgcolor,
                user=request.user,
            )
            post.save()
        else:
            post = Post.objects.create(
                title=title,
                content=content,
                tags=tags,
                categories=categories,
                blog_type=blog_type,
                user=request.user,
            )

            post.save()

        return redirect("bloglist")

    return render(request, "add_blog.html", {"page_title": "Add blog"})


@login_required
@subsciber_required
def edit_blog(request, pst):
    post = Post.objects.get(id=pst)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        try:
            image = request.FILES["image_file"]
        except KeyError:
            image = post.image

        post.title = title
        post.content = content
        post.image = image

        post.save()
        return redirect("bloglist")
    return render(request, "edit_blog.html", blg=post.id)


def add_comment(request, pst):
    post = Post.objects.get(id=pst)

    if request.method == "POST":
        author = request.POST["author"]
        email = request.POST["email"]
        website = request.POST["website"]
        content = request.POST["content"]

        comment = Comment.objects.create(
            author=author, email=email, website=website, content=content, post=post
        )

        comment.save()
        return redirect("blogsingle", pst=pst)

    return None


# TODO: redirect to current user page
@login_required
@subsciber_required
def replay(request, pst):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post.objects.get(id=pst)
        replay = Replay.objects.create(user=request.user, post=post, content=content)
        replay.save()
        return redirect("blogsingle", pst=pst)


def educate(request):
    return render(request, "educate.html")


def list_educate(request, e_type):
    try:
        educate = Educate.objects.filter(educate_type=e_type.lower())
    except Educate.DoesNotExist:
        messages.warning(request, "Can't find educate items with this type.")

    return render(request, "list_educate.html", {"e_types": educate})


def add_educate(request):
    page_title = "Add Educate"
    if request.method == "POST":
        image_file = request.FILES["image_file"]
        title = request.POST.get("title")
        title_arabe = request.POST.get("title_arabe")
        source = request.POST.get("source", "")
        description = request.POST.get("description")
        description_arabe = request.POST.get("description_arabe")
        e_type = request.POST.get("type")

        Educate.objects.create(user=request.user,
                               title=title,
                               title_arabe=title_arabe,
                               description=description,
                               description_arabe=description_arabe,
                               educate_type=e_type,
                               source=source,
                               image=image_file)

        messages.success(request, 'Your form was submited successfully!')
        return redirect("add_educate")

    return render(request, "add_educate.html", {"page_title": page_title})


@login_required
def update_educate(request, edu):
    educate = Educate.objects.get(id=edu)
    if request.method == "POST":
        title = request.POST.get("title")
        title_arabe = request.POST.get("title_arabe")
        description = request.POST.get("description")
        description_arabe = request.POST.get("description_arabe")
        e_type = request.POST.get("type")

        try:
            image_file = request.FILES["image_file"]
        except KeyError:
            image_file = educate.image

        educate.title = title
        educate.title_arabe = title_arabe
        educate.description = description
        educate.description_arabe = description_arabe
        educate.educate_type = e_type
        educate.image = image_file

        educate.save()

        messages.success(request, "successfully update educate")
        return redirect("update_educate", edu=educate.id)

    return render(request, "update_educate.html", {"educate": educate})

def delete_educate(request, edu):
    try:
        Educate.objects.filter(id=edu).delete()
    except Educate.DoesNotExist:
        messages.error(request, "Erro :(, Given Record does not exist in the database")

    return redirect("educate")

@company_required
def company_home(request):
    company = Manufacturer.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            avatar = request.FILES["avatar_image"]
        except KeyError:
            avatar = doctor.user.avatar

        user.avatar = avatar
        user.save()
        return redirect("company")
    return render(request, "company/company.html", {"company": company})


@company_required
def company_orders(request):
    orders = Order.objects.all()
    ods = []
    for order in orders:
        for orderline in order.orderlines.all():
            if orderline.product.owner == request.user:
                ods.append(order)

    return render(
        request, "company/orders.html", {"page_title": "Orders", "orders": ods}
    )


@company_required
def company_overview(request):
    return render(request, "company/overview.html")


@company_required
def company_settings(request):
    return render(request, "company/settings.html")


# TODO: add try/except to catch Errors
@company_required
def company_delete_order(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        Order.objects.get(id=id).delete()
        messages.success(request, "order deleted successfully")
        return redirect("company_orders")


"""
@login_required
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            avatar = request.FILES["avatar_image"]
        except KeyError:
            avatar = doctor.user.avatar

        user.avatar = avatar
        user.save()
        return redirect("doctor_profile")

    return render(request, "doctor_profile.html", {"doctor": doctor})
"""


@login_required
def doctor_home(request):
    return render(request, "doctor/home.html")


@transaction.atomic
def doctor_register(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        specialty = request.POST.get("specialty")
        title = request.POST.get("title")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            first_name=fname, last_name=lname, email=email, password=password,
        )
        user.is_doctor = True
        user.is_active = False
        user.save()
        doctor = Doctor.objects.create(user=user, specialty=specialty, title=title,)
        doctor.save()
        messages.success(request, "Your account was registred successfully!")
        return redirect("doctor_register")
    return render(request, "doctor.html")


@login_required
def doctor_profile(request):
    return render(request, "doctor/profile.html")


@login_required
def doctor_meet(request):
    return render(request, "doctor/meet.html")


@login_required
def doctor_health(request):
    return render(request, "doctor/heath.html")


@login_required
def doctor_update_educate(request, edu):
    educate = Educate.objects.filter(id=edu).first()
    if request.method == "POST":
        title = request.POST.get("title")
        title_arabe = request.POST.get("title_arabe")
        description = request.POST.get("description")
        description_arabe = request.POST.get("description_arabe")
        e_type = request.POST.get("type")

        try:
            image_file = request.FILES["image_file"]
        except KeyError:
            image_file = educate.image

        educate.title = title
        educate.title_arabe = title_arabe
        educate.description = description
        educate.description_arabe = description_arabe
        educate.educate_type = e_type
        educate.image = image_file

        educate.save()

        messages.success(request, "successfully update educate")
        return redirect("/d/educate/")

    return render(request, "doctor/edit.html", {"educate": educate})


@login_required
def doctor_delete_educate(request):
    if request.method == "POST":
        educate_id = request.POST.get("id")
        Educate.objects.filter(id=educate_id).delete()
        return HttpResponse(status=200)


@login_required
def doctor_educate(request):
    data = Educate.objects.filter(user=request.user).all()
    return render(request, "doctor/educate.html", {"data": data})


def doctor_educate_detail(request, e_type):
    try:
        educate_list = Educate.objects.filter(educate_type=e_type.lower())
    except Educate.DoesNotExist:
        messages.warning(request, "Can't find educate items with this type.")
    page = request.GET.get("page", 1)
    paginator = Paginator(educate_list, 5)
    try:
        eds = paginator.page(page)
    except PageNotAnInteger:
        eds = paginator.page(1)
    except EmptyPage:
        eds = paginator.page(educate_list.num_pages)

    return render(request, "list_educate.html", {"eds": eds})


@login_required
def doctor_add_educate(request):
    if request.method == "POST":
        image_file = request.FILES["image_file"]
        title = request.POST.get("title")
        title_arabe = request.POST.get("title_arabe")
        source = request.POST.get("source", "")
        description = request.POST.get("description")
        description_arabe = request.POST.get("description_arabe")
        e_type = request.POST.get("type")

        Educate.objects.create(
            user=request.user,
            title=title,
            title_arabe=title_arabe,
            description=description,
            description_arabe=description_arabe,
            educate_type=e_type,
            source=source,
            image=image_file,
        )

        messages.success(request, "successfully! added new educate")
        return redirect("doctor_educate")

    return render(request, "doctor/add.html")


@login_required
def doctor_send_message(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        subject = request.POST.get("subject", None)
        content = request.POST.get("content", None)

        receiver = User.objects.filter(email=email).first()
        if receiver is not None:
            send_user_email(
                subject,
                email,
                {
                    "content": content,
                    "user": receiver.get_full_name() or receiver.email,
                },
            )
            messages.success(request, "Succcessfully sent message")
            return redirect("doctor_send_message")
        else:
            messages.error(request, "Can't send message, please verify recipient email")
            return redirect("doctor_send_message")
    return render(request, "doctor/send_message.html")


def customer_product(request, f):
    product = CustomerProduct.objects.get(id=f)
    additifs = fake_additifs()

    return render(
        request,
        "customer_product.html",
        {
            "page_title": "Product details",
            "product": product,
            "additifs": additifs,
            "comments": product.commentproduct_set.all(),
        },
    )

def company_product_art(request, f):
    product = ProductArt.objects.get(id=f)

    return render(
        request,
        "company_product_art.html",
        {
            "page_title": "Product details",
            "product": product,
        },
    )


def products(request, f):
    category = Categorie.objects.filter(name=f).first()
    print(category)
    products = []
    if category is not None:
        product_list = ProductArt.objects.all()
        page = request.GET.get("page", 1)
        paginator = Paginator(product_list, 16)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    return render(
        request, "products.html", {"products": products, "page_title": "Products"}
    )


def products_categories(request):
    return render(request, "products_categories.html")


def comment_product(request):
    if request.method == "POST":
        product_id = request.POST.get("id", None)
        comment_text = request.POST.get("comment", None)
        product = CustomerProduct.objects.get(id=product_id)
        if product_id is not None and comment_text is not None:
            comment = CommentProduct(text=comment_text, product=product)
            comment.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

# 

# @login_required
# @subsciber_required
@transaction.atomic  # All or not
def add_product(request):
    if request.method == "POST":
        product = CustomerProduct.objects.create(
            product_name=request.POST.get("product_name", None),
            barcode=request.POST.get("barcode", None),
            tags=request.POST.get("tags", None),
            country=request.POST.get("country", None),
            quantity=request.POST.get("quantity", None),
            ingredients=request.POST.get("ingredients", None),
            energy=request.POST.get("energy_kj", None),
            lipids=request.POST.get("lipids", None),
            fat=request.POST.get("fat", None),
            saturated_fat=request.POST.get("saturated_fat", None),
            carbohydrates=request.POST.get("carbohydrates", None),
            sodium=request.POST.get("sodium", None),
            salt=request.POST.get("salt", None),
            additives=request.POST.get("additives", None),
            protein=request.POST.get("protein", None),
            fiber=request.POST.get("fiber", None),
            sugar=request.POST.get("sugar", None),
            image=save_image_to_folder(request.FILES["product_image"]),
            nutrition_image=save_image_to_folder(request.FILES["nutrition_image"]),
            ingredients_image=save_image_to_folder(request.FILES["ingredients_image"]),
        )

        # save product
        product.save()
        pn = product.product_name
        messages.success(request, "Succcessfully created new product.")
        message = (
            f"We just want to tell you that your product {pn} was created"
            " successfully. and we want you to keep an eye on your inbox,"
            " to get approval message. Have a nice day my friend."
        )
        context = {
            "user": request.user.get_full_name or "akala user",
            "message": message,
        }
        # TODO: use celery to send these message or user job handler or threaded methods
        # send_email("New Product was created", "adhemmbarkia@gmail.com", context)
        return redirect("add_product")

    return render(request, "add_product.html", {"page_title": "New Product"})



# NOTICE: created file 'search_result' if a problem accured
# and it's related to it, then please verify your code
def search_product(request, code):
    result = CustomerProduct.objects.filter(barcode=code).first()
    if result is None:
        messages.error(request, "Not Found")
        return redirect("index")
    return render(
        request,
        "product_result.html",
        {"product": result, "page_title": "Search result"},
    )



def doctor_list(rq):
    doctors = Doctor.objects.all()
    return render(rq, "doctor_list.html", {"doctors":doctors, "page_title": "Doctors"})
