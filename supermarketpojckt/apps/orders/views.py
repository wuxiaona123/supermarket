from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    def get(self, request):
        return HttpResponse('订单首页 get')

    def post(self, request):
        return HttpResponse('订单首页 post')
