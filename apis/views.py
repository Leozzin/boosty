from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from food.models import User
from .serializers import *

# ------------------------------------------------------- -
# -------------------------USERS------------------------- #
# ------------------------------------------------------- #
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAdminUser]

class UserRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAdminUser]

# ------------------------------------------------------- #
# -------------------------POSTS------------------------- #
# ------------------------------------------------------- #
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# ------------------------------------------------------- #
# ------------------------MESSAGE------------------------ #
# ------------------------------------------------------- #
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# ------------------------------------------------------- #
# ------------------------COMMENT------------------------ #
# ------------------------------------------------------- #
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# ------------------------------------------------------- #
# ------------------------REPLAY------------------------- #
# ------------------------------------------------------- #
class ReplayList(generics.ListCreateAPIView):
    queryset = Replay.objects.all()
    serializer_class = ReplaySerializer

class ReplayRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Replay.objects.all()
    serializer_class = ReplaySerializer

# ------------------------------------------------------- #
# -----------------------ALLERGIE------------------------ #
# ------------------------------------------------------- #
class AllergieList(generics.ListCreateAPIView):
    queryset = Allergie.objects.all()
    serializer_class = AllergieSerializer

class AllergieRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Allergie.objects.all()
    serializer_class = AllergieSerializer

# ------------------------------------------------------- #
# ---------------------HEALTH_PROBLEM-------------------- #
# ------------------------------------------------------- #
class HealthProblemList(generics.ListCreateAPIView):
    queryset = health_problem.objects.all()
    serializer_class = HealthProblemSerializer

class HealthProblemRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = health_problem.objects.all()
    serializer_class = HealthProblemSerializer

# ------------------------------------------------------- #
# -----------------------CATEGORIE----------------------- #
# ------------------------------------------------------- #
class CategorieList(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class CategorieRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

# ------------------------------------------------------- #
# ----------------------SUBCATEGORY---------------------- #
# ------------------------------------------------------- #
class SubCategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class SubCategoryRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

# ------------------------------------------------------- #
# ------------------------PRODUCT------------------------ #
# ------------------------------------------------------- #
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ------------------------------------------------------- #
# ---------------------PRODUCTDEATAIL-------------------- #
# ------------------------------------------------------- #
class ProductDetailList(generics.ListCreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer

class ProductDetailRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer

# ------------------------------------------------------- #
# --------------------------BLOG------------------------- #
# ------------------------------------------------------- #
class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

# ------------------------------------------------------- #
# -------------------------RECIPE------------------------ #
# ------------------------------------------------------- #
class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

# ------------------------------------------------------- #
# ---------------------RecipeComment--------------------- #
# ------------------------------------------------------- #
class RecipeCommentList(generics.ListCreateAPIView):
    queryset = RecipeComment.objects.all()
    serializer_class = RecipeCommentSerializer

class RecipeCommentRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeComment.objects.all()
    serializer_class = RecipeCommentSerializer

# ------------------------------------------------------- #
# ---------------------RecipeRating---------------------- #
# ------------------------------------------------------- #
class RecipeRatingList(generics.ListCreateAPIView):
    queryset = RecipeRating.objects.all()
    serializer_class = RecipeRatingSerializer

class RecipeRatingRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeRating.objects.all()
    serializer_class = RecipeRatingSerializer

# ------------------------------------------------------- #
# ------------------------PAYMENT------------------------ #
# ------------------------------------------------------- #
class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# ------------------------------------------------------- #
# -----------------------ORDERLINE----------------------- #
# ------------------------------------------------------- #
class OrderLineList(generics.ListCreateAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

class OrderLineRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

# ------------------------------------------------------- #
# -------------------------ORDER------------------------- #
# ------------------------------------------------------- #
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# ------------------------------------------------------- #
# -----------------------CONTACT------------------------- #
# ------------------------------------------------------- #
class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

# ------------------------------------------------------- #
# -------------------CUSTOMERPRODUCT--------------------- #
# ------------------------------------------------------- #
class CustomerProductList(generics.ListCreateAPIView):
    queryset = CustomerProduct.objects.all()
    serializer_class = CustomerProductSerializer

class CustomerProductRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProduct.objects.all()
    serializer_class = CustomerProductSerializer

# ------------------------------------------------------- #
# -------------------CUSTOMERHEALTH---------------------- #
# ------------------------------------------------------- #
class CustomerHealthList(generics.ListCreateAPIView):
    queryset = CustomerHealth.objects.all()
    serializer_class = CustomerHealthSerializer

class CustomerHealthRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerHealth.objects.all()
    serializer_class = CustomerHealthSerializer

# ------------------------------------------------------- #
# -------------------COMMENTPRODUCT---------------------- #
# ------------------------------------------------------- #
class CommentProductList(generics.ListCreateAPIView):
    queryset = CommentProduct.objects.all()
    serializer_class = CommentProductSerializer

class CommentProductRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentProduct.objects.all()
    serializer_class = CommentProductSerializer

# ------------------------------------------------------- #
# -------------------PRODUCTCATEGORY--------------------- #
# ------------------------------------------------------- #
class ProductCategoryList(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductCategoryRud(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer