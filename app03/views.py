import hashlib
import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Food
from app02.views import handle_exception_response
from .models import Shop
# Create your views here.

def showShops(request):
    try:
        shops = Shop.objects.all()
        result = list(shops.values())
        return JsonResponse(result,safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({"error": "No shops found"}, status=404)
    except Exception as e:
        return handle_exception_response(e)



@csrf_exempt
def addShop(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        enterData = data.get('enterData')
        shopNum = data.get('shopNum')
        name = data.get('name')
        legalPerson = data.get('legalPerson')
        phoneNum = data.get('phoneNum')
        address = data.get('address')
        password = data.get('shopNum') + legalPerson
        if enterData and shopNum and name and legalPerson and address and phoneNum:
            Shop.objects.create(enterData=enterData, name=name, phoneNum=phoneNum, shopNum=shopNum, address=address,legalPerson=legalPerson,password=password)
            return JsonResponse(True,safe=False)
        else:
            return JsonResponse(False,safe=False)
    else:
        return JsonResponse(False,safe=False)

@csrf_exempt
@require_http_methods(['DELETE'])
def removeShop(request):
    try:
        shopNum = request.GET.get('shopNum')
        shop = Shop.objects.get(shopNum=shopNum)
        if shop:
            shop.delete()
            return JsonResponse(True,safe=False)
        else:
            JsonResponse(False, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse(False,safe=False)


def login(request):
    shopNum = request.GET.get("shopNum")
    encrypted_password = request.GET.get("password")  # 接收加密后的密码

    try:
        data = Shop.objects.get(shopNum=shopNum)  # 从数据库中获取数据
        # 对数据库中的密码字段进行加密，然后与前端传来的加密密码进行比较
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        if encrypted_password == password_hash:
            return JsonResponse(True, safe=False)  # 返回JSON格式的数据给前端
        else:
            return JsonResponse(False,safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(False,safe=False)



from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        save_path = os.path.join('D:\\Project\\super\\vue_super', 'src', 'static', filename)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        img = "/src/static/"+filename

        return JsonResponse({'img':img},safe=False)  # 直接返回字符串
    else:
        return JsonResponse(False,safe=False) # 返回错误消息字符串


@csrf_exempt
def addFood(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        explain = data.get('explain')
        name = data.get('name')
        price = data.get('price')
        shopNum = data.get('shopNum')
        img = data.get('img')

        if explain and name and price and shopNum and img:
            Food.objects.create(explain=explain, name=name, price=price, shopNum=shopNum,img=img,sellOut=True)
            return JsonResponse(True,safe=False)
        else:
            return JsonResponse(False,safe=False)
    else:
        return JsonResponse(False,safe=False)

def showFoods(request):
    try:
        shopNum = request.GET.get('shopNum')
        foods = Food.objects.filter(shopNum=shopNum).all()
        result = list(foods.values())
        return JsonResponse(result,safe=False)
    except Food.DoesNotExist:
        return JsonResponse({"error": "No shops found"}, status=404)
    except Exception as e:
        return handle_exception_response(e)

@csrf_exempt
def updateInfo(request):
    if request.method == 'PUT':
        # 使用 get 方法获取请求参数，避免 KeyError 错误
        data = json.loads(request.body)
        shopNum = data.get('shopNum')
        name = data.get('name')
        phoneNum = data.get('phoneNum')
        legalPerson = data.get('legalPerson')
        address = data.get('address')
        password = data.get('password')
        main = data.get('main')
        # 获取对应的店铺对象
        shop = Shop.objects.filter(shopNum=shopNum).first()

        # 如果店铺对象存在，则更新信息
        if shop:
            # 更新对象的字段并保存
            shop.name = name
            shop.phoneNum = phoneNum
            shop.legalPerson = legalPerson
            shop.address = address
            shop.password = password
            shop.main = main
            shop.save()
            # 返回 JSON 响应
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def getShop(request):
    shopNum = request.GET.get('shopNum')

    # 使用 get_object_or_404 来获取对象，确保查询结果存在，否则返回 404 响应
    shop = get_object_or_404(Shop, shopNum=shopNum)

    # 将商店对象的属性直接映射到字典，避免重复定义
    result = {
        'name': shop.name,
        'phoneNum': shop.phoneNum,
        'legalPerson': shop.legalPerson,
        'address': shop.address,
        'img': shop.img,
        'sale': shop.sale,
        'password': shop.password,
        'main': shop.main,
    }

    return JsonResponse(result)

@csrf_exempt
def updateSellOut(request):
    if request.method != 'PUT':
        return JsonResponse(False,safe=False)

    data = json.loads(request.body)
    food_id = data.get('id')

    if not food_id:
        return JsonResponse(False,safe=False)

    # 检查是否存在对应的食品对象
    if Food.objects.filter(id=food_id).exists():
        # 获取食品对象并更新状态
        food = Food.objects.get(id=food_id)
        food.sellOut = not food.sellOut
        food.save()
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False,safe=False)


@csrf_exempt
@require_http_methods(['DELETE'])
def removeFood(request):
    try:
        id = request.GET.get('id')
        food = Food.objects.get(id=id)
        if food:
            food.delete()
            return JsonResponse(True, safe=False)
        else:
            JsonResponse(False, safe=False)
    except Food.DoesNotExist:
        return JsonResponse(False, safe=False)


@csrf_exempt
def uploadHead(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        save_path = os.path.join('D:\\Project\\super\\vue_super', 'src', 'static', filename)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        img = "/src/static/" + filename
        shopNum = request.POST.get('shopNum')

        shop = Shop.objects.filter(shopNum=shopNum).first()
        shop.img = img
        shop.save()
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)

@csrf_exempt
def addSale(request):
    if request.method == 'PUT':
        shopNum = request.GET.get('shopNum')
        if shopNum:
            shop = Shop.objects.filter(shopNum=shopNum).first()
            if shop:
                shop.sale += 1
                shop.save()
                return JsonResponse(True,safe=False)
            else:
                return JsonResponse(False,safe=False)

        else:
            return JsonResponse(False,safe=False)
    else:
        return JsonResponse(False,safe=False)


def getAllShopInfo(request):
    # 用于存储所有商店信息的列表
    infos = []

    # 获取所有商店对象
    shops = Shop.objects.all()

    # 遍历每个商店
    for shop in shops:
        # 创建新的字典对象来存储当前商店的信息
        shop_info = {}
        shop_info['name'] = shop.name
        shop_info['legalPerson'] = shop.legalPerson
        shop_info['address'] = shop.address
        shop_info['img'] = shop.img
        shop_info['shopNum'] = shop.shopNum
        # 获取当前商店的所有食物对象
        foods = Food.objects.filter(shopNum=shop.shopNum)

        # 将食物信息存储在列表中
        food_list = []
        for food in foods:
            food_info = {
                'name': food.name,
                'price': food.price,
                'explain': food.explain
            }
            food_list.append(food_info)

        # 将食物列表存储在当前商店信息字典中
        shop_info['foods'] = food_list

        # 将当前商店信息字典添加到总信息列表中
        infos.append(shop_info)

    # 返回JSON响应
    return JsonResponse(infos, safe=False)


def checkShops(request):
    main = request.GET.get('main')
    try:
        shops = Shop.objects.filter(main=main).all()
        result = list(shops.values())
        return JsonResponse(result, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({"error": "No shops found"}, status=404)
    except Exception as e:
        return handle_exception_response(e)

# @csrf_exempt
# def updateMain(request):
#     data = json.loads(request.body)
#     shopNum = data.get('shopNum')
#     main = data.get('main')
#
#     # 检查商店是否存在
#     shop = Shop.objects.filter(shopNum=shopNum).first()
#     if not shop:
#         return JsonResponse({'error': 'Shop not found'}, status=404)
#
#     # 更新主要属性并保存
#     shop.main = main
#     shop.save()
#
#     return JsonResponse({'success': True})

