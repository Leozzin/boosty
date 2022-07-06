from django.conf.urls import url
from django.urls import path
from . import views
from food.bot import ChatBotApi
from django.conf.urls import handler404

handler404 = "food.views.handler404"


urlpatterns = [
    path("", views.index, name="index"),
    path("recipelist/", views.recipelist, name="recipelist"),
    path("recipesingle/<int:rcp>/", views.recipesingle, name="recipesingle"),
    path("", views.recipeindex, name="recipeindex"),
    path("recipesubmit/", views.recipesubmit, name="recipesubmit"),
    path("archive/", views.archive, name="archive"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register"),
    path("gauge/", views.preview_gauge, name="gauge"),
    path("not_found/", views.not_found, name="404"),
    path("search/", views.search, name="search"),
    path("profile/", views.profile, name="profile"),
    path("company/register/", views.company_auth, name="company_auth"),
    path("educate/", views.educate, name="educate"),
    path("update_educate/<int:edu>/",
        views.update_educate,
        name="update_educate"),
    path("delete_educate/<int:edu>/",
        views.delete_educate,
        name="delete_educate"),
    path("list_educate/<str:e_type>/",
        views.list_educate,
        name="list_educate"),
    path("store/", views.store, name="store"),
    path("bloglist/", views.bloglist, name="bloglist"),
    path("blogsingle/<int:pst>/", views.blogsingle, name="blogsingle"),
    path("add_blog/", views.add_blog, name="add_blog"),
    path("edit_blog/<int:pst>/", views.edit_blog, name="edit_blog"),
    path("replay/<int:pst>/", views.replay, name="replay"),
    path("resipecomment/<int:rcp>/", views.recipecomment, name="recipecomment"),
    path("resipereplay/<int:rcp>/", views.recipereplay, name="recipereplay"),
    path("reciperating/", views.reciperating, name="reciperating"),
    path("like/", views.like, name="like"),
    path("dislike/", views.dislike, name="dislike"),
    path("recipelike/", views.recipe_like, name="recipelike"),
    path("recipedislike/", views.recipe_dislike, name="recipedislike"),
    path("store/product/<int:id>/", views.product, name="product"),
    path("store/cart/", views.cart, name="basket"),
    path("store/cart/<int:id>", views.remove_product_cart, name="remove_product_cart"),
    path("store/add_to_cart/", views.add_to_cart, name="add_to_basket"),
    path("store/cart/update/", views.update_cart_product, name="update_cart_product"),
    path("store/checkout/", views.checkout, name="create_order"),
    path("store/cart/to_edit/", views.to_edit, name="to_edit"),
    path(
        "c/products/edit/<int:p>/",
        views.company_edit_product,
        name="company_edit_product",
    ),
    path("c/company/", views.company_home, name="company"),
    path("c/orders/", views.company_orders, name="orders"),
    path("c/products/", views.company_products, name="products"),
    path("c/overview/", views.company_overview, name="overview"),
    path("c/settings/", views.company_settings, name="settings"),
    path("c/products/add/", views.company_add_product, name="company_add_product"),
    path(
        "c/products/delete/",
        views.company_delete_product,
        name="company_delete_product",
    ),
    path("c/products/add/", views.company_add_product, name="company_add_product"),
    # DOCOTR
    path("health/", views.health, name="health"),
    path("body/", views.body, name="body"),
    path("d/profile/", views.doctor_profile, name="doctor_profile"),
    path("d/home/", views.doctor_home, name="doctor_home"),
    path("d/register/", views.doctor_register, name="doctor_register"),
    path("d/educate/", views.doctor_educate, name="doctor_educate"),
    path("d/educate/add/", views.doctor_add_educate, name="add_educate"),
    path("d/meet/", views.doctor_meet, name="doctor_meet"),
    path("d/heath/", views.doctor_health, name="doctor_health"),
    path("d/message/", views.doctor_send_message, name="doctor_send_message"),
    path(
        "d/educate/update/<int:edu>/",
        views.doctor_update_educate,
        name="update_educate",
    ),
    path("add_comment/<int:pst>/", views.add_comment, name='add_comment'),
    path("d/educate/delete/", views.doctor_delete_educate, name="delete_educate",),
    path("p/product/<int:f>", views.customer_product, name="customer_product"),
    path("p/product-art/<int:f>", views.company_product_art, name="company_product_art"),
    path("p/products/<str:f>", views.products, name="products"),
    path("p/categories", views.products_categories, name="products_categories"),
    path("p/comment", views.comment_product, name="comment_product"),
    path("p/product/add", views.add_product, name="add_product"),
    path("p/compare", views.compare, name="compare"),
    path("h/add", views.health_add, name="health_add"),
    path("doctors/", views.doctor_list, name="doctors"),
    path("p/search/<str:code>", views.search_product, name="search_product"),
    path("api/bot/", ChatBotApi.as_view(), name="chatterbot")
    #path("p/search/result/<>")
]
