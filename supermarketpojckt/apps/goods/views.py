from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    def post(self,request):
        return HttpResponse('商品首页post')
    def get(self,request):
        return render(request,'goods/index.html')