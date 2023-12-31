from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from celery.result import AsyncResult
from .tasks.c_text import res
from rest_framework import permissions

# Create your views here.




class Start(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        lat = request.data.get('latitude', None)  
        lon = request.data.get('longitude', None)   
        range = request.data.get('genre', None)
        budget = request.data.get('budget', None)
        genre = request.data.get('genre', None)
        otheroptions = request.data.get('otheroptions', None)
        if lat is not None and lon is not None:
            task = res.delay(lat, lon, range, budget, genre, otheroptions)
            return Response({'task_id': task.id}, status=202)
        else :
            return Response({"error": "ポイントを選択してください"}, status=status.HTTP_400_BAD_REQUEST)

    

class Poll(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        task_id = request.data.get('task_id', None)
        if task_id is None:
            return Response({'error': 'Missing task_id parameter'}, status=400)
        task = AsyncResult(task_id)
        if task.ready():
            return Response({'state': 'READY', 'result': task.result})
        else:
            return Response({'state': 'PENDING'})

