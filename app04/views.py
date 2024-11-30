import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Notice
# Create your views here.
@csrf_exempt
def addNotice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data.get('msg')
        if msg:
            try:
                Notice.objects.create(msg=msg)
                return JsonResponse(True,safe=False)
            except Exception as e:
                return JsonResponse(False,safe=False)
        else:
            return JsonResponse(False,safe=False)
    else:
        return JsonResponse(False,safe=False)

def getNotice(request):
    max_tuple = Notice.objects.latest('id')
    msg = max_tuple.msg
    data = {
        'msg': msg
    }
    return JsonResponse(data,safe=False)
