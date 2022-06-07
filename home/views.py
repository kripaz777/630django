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
