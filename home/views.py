from django.shortcuts import render
from django.views import View

from .models import *
# Create your views here.

class BaseView(View):
	views = {}
	



class HomeView(BaseView):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories'] = SubCategory.objects.all()
		self.views['new_products'] = Product.objects.filter(labels = 'new')
		self.views['hot_products'] = Product.objects.filter(labels = 'hot')
		self.views['offer_products'] = Product.objects.filter(labels = 'offer')
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		return render(request,'index.html',self.views)

