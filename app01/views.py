import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Manager

import hashlib

def login(request):
    # 从请求中获取员工号和加密后的密码
    employeeNum = request.GET.get("employeeNum")
    encrypted_password = request.GET.get("password")  # 接收加密后的密码

    try:
        # 查询数据库以获取员工信息
        data = Manager.objects.get(employeeNum=employeeNum)  # 从数据库中获取数据
        # 对数据库中的密码字段进行加密，然后与前端传来的加密密码进行比较
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        # 验证密码是否匹配
        if encrypted_password == password_hash:
            return JsonResponse(True, safe=False)  # 返回JSON格式的数据给前端
        else:
            return JsonResponse(False,safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(False,safe=False)


