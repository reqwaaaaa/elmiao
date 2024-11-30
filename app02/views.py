import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_http_methods

from .models import Worker

# Create your views here.
def handle_exception_response(e):
    # 处理其他异常情况，可以记录错误日志等操作
    # Handle other exceptions, log the error, etc.
    return JsonResponse({"error": str(e)}, status=500)  # 返回包含错误信息的JSON响应，并设置状态码为500

def showWorkers(request):
    try:
        # 从数据库中获取所有的Worker对象
        workers = Worker.objects.all()
        # Convert workers to a list
        # 将Worker对象转换为列表
        workers_list = list(workers.values())
        # 返回JSON格式的数据给前端，表示成功获取所有worker信息
        return JsonResponse(workers_list, safe=False)
    except Worker.DoesNotExist:
        # 如果未找到任何worker，则返回包含错误信息的JSON响应，并设置状态码为404
        return JsonResponse({"error": "No workers found"}, status=404)
    except Exception as e:
        # 对其他异常情况进行处理，调用handle_exception_response函数
        return handle_exception_response(e)


@csrf_exempt
def addWorker(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employeeNum = data.get('employeeNum')
        name = data.get('name')
        phoneNum = data.get('phoneNum')
        gender = data.get('gender')
        salary = data.get('salary')


        if employeeNum and name and phoneNum and gender and salary:
            # Create and save a new Worker object
            Worker.objects.create(employeeNum=employeeNum, name=name, phoneNum=phoneNum, gender=gender, salary=salary)
            return JsonResponse(True,safe=False)  # Return success as JSON response
        else:
            return JsonResponse(False,safe=False)
    else:
        return JsonResponse(False,safe=False)

@csrf_exempt
@require_http_methods(['DELETE'])
def removeWorker(request):
    try:
        employeeNum = request.GET.get('employeeNum')
        worker = Worker.objects.get(employeeNum=employeeNum)
        if worker:
            worker.delete()
            return JsonResponse(True,safe=False)
        else:
            JsonResponse(False, safe=False)
    except Worker.DoesNotExist:
        return JsonResponse(False,safe=False)



