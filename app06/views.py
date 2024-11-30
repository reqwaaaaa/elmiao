import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from app06.models import Order, Foods, Eval


# Create your views here.
def addOrder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        orderNum = data.get('orderNum')
        return JsonResponse(True, safe=False)


def getOrders(request):
    shopNum = request.GET.get('shopNum')

    # 获取相关订单
    orders = Order.objects.filter(shopNum=shopNum)

    # 获取相关食品
    orders_with_foods = []
    for order in orders:
        # 获取订单关联的食品
        foods = Foods.objects.filter(orderNum=order.orderNum)

        # 将订单和食品存入字典
        order_dict = {
            'orderNum': order.orderNum,
            'shopNum': order.shopNum,
            'shopName': order.shopName,
            'shopPhone': order.shopPhone,
            'address0': order.address0,
            'address1': order.address1,
            'stuPhone': order.stuPhone,
            'note': order.note,
            'total': order.total,
            'status': order.status,
            # 其他订单字段...
            'foods': list(foods.values())  # 将食品转换为字典列表并存入订单字典中
        }

        # 将订单字典添加到列表中
        orders_with_foods.append(order_dict)

    # 返回 JSON 响应
    return JsonResponse(orders_with_foods, safe=False)


@csrf_exempt
def updateStatus(request):
    if request.method == 'PUT':
        # 从请求体中获取数据
        data = json.loads(request.body)
        orderNum = data.get('orderNum')
        order = Order.objects.filter(orderNum=orderNum).first()
        if order:
            order.status = True
            order.save()
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def getTotalOfAllDay(request):
    shop_num = request.GET.get('shopNum')

    if not shop_num:
        return JsonResponse({'error': 'Shop number is required.'}, status=400)

    total_amount = Order.objects.filter(shopNum=shop_num, status=True).aggregate(total_amount=Sum('total'))[
                       'total_amount'] or 0

    return JsonResponse({'total': total_amount}, safe=False)


def getEval(request):
    shop_num = request.GET.get('shopNum')

    if not shop_num:
        return JsonResponse({'error': 'Missing shopNum parameter'}, status=400)

    try:
        eval_instances = Eval.objects.filter(shopNum=shop_num)
        eval_data = []
        for eval_instance in eval_instances:
            eval_dict = {
                'shopNum': eval_instance.shopNum,
                'img': eval_instance.img,
                'msg': eval_instance.msg,
                'starNum': eval_instance.starNum
                # 添加其他字段
            }
            eval_data.append(eval_dict)
        return JsonResponse(eval_data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Evaluation not found'}, status=404)


@csrf_exempt
def addOrder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        orderNum = data.get('orderNum')
        shopNum = data.get('shopNum')
        shopName = data.get('shopName')
        shopPhone = data.get('shopPhone')
        address0 = data.get('address0')
        address1 = data.get('address1')
        stuPhone = data.get('stuPhone')
        note = data.get("note")
        total = data.get('total')
        balance = int(data.get('balance'))
        if orderNum and shopNum and shopName and shopPhone and address0 and address1 and stuPhone and total and balance >= total:
            Order.objects.create(orderNum=orderNum, shopNum=shopNum, shopPhone=shopPhone, shopName=shopName,
                                 address0=address0, address1=address1, stuPhone=stuPhone, note=note, total=total)
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


@csrf_exempt
def addFoods(request):
    try:
        data = json.loads(request.body)
        order_num = data.get('orderNum')
        foods = data.get('foods')

        for food in foods:
            # Ensure the food object exists
            subtotal = food['quantity'] * food['price']
            Foods.objects.create(orderNum=order_num, name=food['name'], num=food['quantity'], subtotal=subtotal)
    except Exception as e:
        # Handle any unexpected exceptions
        return JsonResponse(True, safe=False)

    return JsonResponse(True, safe=False)


def getOrderByPhone(request):
    phoneNum = request.GET.get('phone')

    # 获取相关订单
    orders = Order.objects.filter(stuPhone=phoneNum)

    # 获取相关食品
    orders_with_foods = []
    for order in orders:
        # 获取订单关联的食品
        foods = Foods.objects.filter(orderNum=order.orderNum)

        # 将订单和食品存入字典
        order_dict = {
            'orderNum': order.orderNum,
            'shopNum': order.shopNum,
            'shopName': order.shopName,
            'shopPhone': order.shopPhone,
            'address0': order.address0,
            'address1': order.address1,
            'stuPhone': order.stuPhone,
            'note': order.note,
            'total': order.total,
            'status': order.status,
            # 其他订单字段...
            'foods': list(foods.values())  # 将食品转换为字典列表并存入订单字典中
        }

        # 将订单字典添加到列表中
        orders_with_foods.append(order_dict)
    # 返回 JSON 响应
    return JsonResponse(orders_with_foods, safe=False)


@csrf_exempt
@require_POST
def addEval(request):
    try:
        data = json.loads(request.body)
        shop_num = data.get('shopNum')
        img = data.get('img')
        msg = data.get('msg')
        star_num = data.get('starNum')

        if shop_num is None or img is None or msg is None or star_num is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        Eval.objects.create(shopNum=shop_num, img=img, msg=msg, starNum=star_num)
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)


from django.shortcuts import render

# Create your views here.
