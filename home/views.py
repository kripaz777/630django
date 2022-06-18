from django.shortcuts import render,redirect
from django.views import View

from .models import *
# Create your views here.

class BaseView(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['subcategories'] = SubCategory.objects.all()

class HomeView(BaseView):
	def get(self,request):
		self.views
		self.views['new_products'] = Product.objects.filter(labels = 'new')
		self.views['hot_products'] = Product.objects.filter(labels = 'hot')
		self.views['offer_products'] = Product.objects.filter(labels = 'offer')
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		return render(request,'index.html',self.views)


class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		self.views['subcat_products'] = Product.objects.filter(subcategory_id = subcat_id)
		return render(request,'subcategory.html',self.views)


class DetailView(BaseView):
	def get(self,request,slug):
		self.views['detail_products'] = Product.objects.filter(slug = slug)
		return render(request,'single.html',self.views)

from django.db.models import Q
class SearchView(BaseView):
	def get(self,request):
		query = request.GET['query']
		if query == '':
			return redirect('/')
		else:	
			lookups = Q(name__icontains = query) | Q(description__icontains = query)
			self.views['search_result'] = Product.objects.filter(lookups).distinct()
			self.views['search_for'] = query
			return render(request,'search.html',self.views)

from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']

		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already used.')
				return redirect('/signup')

			elif User.objects.filter(email = email).exists():
				messages.error(request,'The email is already used.')
				return redirect('/signup')

			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
				user.save()
				return redirect('/')


		else:
			messages.error(request,'The password does not match')
			return redirect('/signup')

	return render(request,'register.html')



def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.error(request,'Username or password does not match.')
			return redirect('/login')

	return render(request,'login.html')


def logout(request):
	auth.logout(request)
	return redirect('/')

def cal_cart(slug,username):
	price = Product.objects.get(slug = slug).price
	discounted_price = Product.objects.get(slug = slug).discounted_price
	if Cart.objects.filter(username = username,slug = slug,checkout = False).exists():
		quantity = Cart.objects.get(username = username,slug = slug,checkout = False).quantity
		quantity = quantity+1
	else:
		quantity = 1

	if discounted_price > 0:
		original_price = discounted_price
		total = original_price*quantity
	else:
		original_price = price
		total = original_price*quantity

	return total,original_price,quantity

def cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(username = username,slug = slug,checkout = False).exists():
		total,original_price,quantity = cal_cart(slug,username)
		Cart.objects.filter(username = username,slug = slug,checkout = False).update(quantity = quantity,total = total)

	else:
		total,original_price,quantity = cal_cart(slug,username)
		data = Cart.objects.create(
			username = username,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0],
			total = original_price
			)
		data.save()
	return redirect('/mycart')

def delete_cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(username = username,slug = slug,checkout = False).exists():
		Cart.objects.filter(username = username,slug = slug,checkout = False).delete()
		return redirect('/mycart')	

def remove_product(request,slug):
	username = request.user.username
	price = Product.objects.get(slug = slug).price
	discounted_price = Product.objects.get(slug = slug).discounted_price
	quantity = Cart.objects.get(username = username,slug = slug,checkout = False).quantity
	if quantity >1:
		quantity = quantity-1
		if discounted_price > 0:
			original_price = discounted_price
			total = original_price*quantity
		else:
			original_price = price
			total = original_price*quantity

		Cart.objects.filter(username = username,slug = slug,checkout = False).update(quantity = quantity,total = total)
		return redirect('/mycart')
	return redirect('/mycart')


class CartView(BaseView):
	def get(self,request):
		username = request.user.username
		self.views['cart_view'] = Cart.objects.filter(username = username,checkout = False)
		return render(request,'wishlist.html',self.views)


# -------------------------------------API------------------------------------------------
from .serializers import *
from rest_framework import serializers, viewsets

# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


import django_filters.rest_framework
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class ProductFilterViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['id','category','subcategory','labels','status']
    ordering_fields = ['price','id','name']
    search_fields = ['name','description']


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views  import APIView

class CRUDItemViewSet(APIView):
	def get_object(self,pk):
		try:
			return Product.objects.get(pk = pk)
		except:
			print("The id does not exists.")
	def get(self,request,pk,format = None):
			product_data = self.get_object(pk)
			serializer = ProductSerializer(product_data)
			return Response(serializer.data)
	def post(self,request,pk,format = None):
		serializer = ProductSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status':"The value is posted"})

	def put(self,request,pk,format = None):
		product_data = self.get_object(pk)
		serializer = ProductSerializer(product_data,data = request.data,partial = True)
		if serializer.is_valid():
			# (serializer.data).update(request.data)
			serializer.save()
			return Response(serializer.data)
		return Response({'status':"The value is updated"})

	def delete(self,request,pk):
		try:
			Product.objects.filter(id = pk).delete()
			return Response({"status":"The object is deleted"})
		except:
			return Response({"status":"The object is already deleted"})