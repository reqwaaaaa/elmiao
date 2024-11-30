import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app05.models import Student


# Create your views here.
def getInfo(request):
    # 获取请求参数
    phone_num = request.GET.get('phoneNum')

    # 验证参数是否存在
    if not phone_num:
        return JsonResponse({'error': 'Missing phoneNum parameter'}, status=400)

    try:
        # 查询学生对象
        student = Student.objects.get(phone=phone_num)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # 构造响应数据
    data = {
        'phone': student.phone,
        'account': student.account,
        'password': student.password,
        'address': student.address,
        'balance': student.balance,
    }

    # 返回响应
    return JsonResponse(data)

@csrf_exempt
def newStu(request):
    if request.method != 'POST':
        return JsonResponse(False,safe=False)
    data = json.loads(request.body)
    phone = data.get('phone')
    account = data.get('account')
    password = data.get('password')
    address = data.get('address')
    balance = data.get('balance')
    Student.objects.create(phone=phone,account=account,password=password,address=address,balance=balance)
    return JsonResponse(True,safe=False)


@csrf_exempt
def updateBalance(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        change = data.get('change')
        phone = data.get('phone')
        # 验证参数是否存在
        if not change or not phone:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        # 查询学生对象
        stu = Student.objects.filter(phone=phone).first()

        # 如果找不到学生对象，返回404错误
        if not stu:
            return JsonResponse({'error': 'Student not found'}, status=404)

        # 更新余额
        stu.balance -= change
        stu.save()

        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def updateStuInfo(request):
    data = json.loads(request.body)
    phone = data.get('phone')
    balance = data.get('balance')
    account = data.get('account')
    address = data.get('address')

    # 尝试直接获取符合条件的学生对象
    stu = Student.objects.filter(phone=phone).first()

    # 如果找不到学生对象，则返回错误响应
    if not stu:
        return JsonResponse({'error': '学生对象不存在'}, status=404)

    # 更新学生对象的信息
    stu_info = {
        'balance': balance,
        'phone': phone,
        'account': account,
        'address': address
    }

    # 使用 update() 方法更新学生对象
    Student.objects.filter(phone=phone).update(**stu_info)

    # 返回成功响应
    return JsonResponse(True,safe=False)

