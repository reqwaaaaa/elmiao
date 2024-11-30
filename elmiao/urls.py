"""
URL configuration for elmiao project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app01 import views as views01
from app02 import views as views02
from app03 import views as views03
from app04 import views as views04
from app05 import views as views05

from app06 import views as views06

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('manager/login', views01.login),
    path('show/workers',views02.showWorkers),
    path('show/shops',views03.showShops),
    path('add/worker',views02.addWorker),
    path('remove/worker',views02.removeWorker),
    path('add/shop',views03.addShop),
    path('remove/shop',views03.removeShop),
    path('add/notice',views04.addNotice),
    path('shop/login',views03.login),
    path('add/food', views03.addFood),
    path('api/upload/', views03.upload, name='upload_file'),
    path('show/foods',views03.showFoods),
    path('add/order',views06.addOrder),
    path('get/orders',views06.getOrders),
    path('update/status',views06.updateStatus),
    path('get/day/total',views06.getTotalOfAllDay),
    path('get/evals',views06.getEval),
    path('update/shopinfo',views03.updateInfo),
    path('get/shop',views03.getShop),
    path('update/sellout',views03.updateSellOut),
    path('remove/food',views03.removeFood),
    path('update/head/',views03.uploadHead),
    path('add/order',views06.addOrder),
    path('add/foods',views06.addFoods),
    path('add/sale',views03.addSale),
    path('get/stu/info',views05.getInfo),
    path('get/orders/by/phone',views06.getOrderByPhone),
    path('new/stu',views05.newStu),
    path('update/balance',views05.updateBalance),
    path('get/notice',views04.getNotice),
    path('get/all/shop/info',views03.getAllShopInfo),
    path('update/stu/info',views05.updateStuInfo),
    path('check/shops',views03.checkShops),
    path('add/eval',views06.addEval),
]

