from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Record
#from news.models import News
from .serializers import RecordSerializer
from news.models import News
from news.views import *

# POST냐 GET이냐에 따라 같은 uri지만, 다른 함수 실행
# @api_view(['POST', 'GET'])
# def calendar_handler(request, date):
#      if request.method == 'POST':
#          return create_record(request, date)
#      elif request.method == 'GET':
#          return home(request, date)

# 채팅(여기서는 기사 요약..?) 치기
@api_view(['POST'])
def create_record(request):
  serializer = RecordSerializer(data=request.data)
  if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  serializer.save()
  return Response(serializer.data, status=status.HTTP_201_CREATED)

# 날짜 별 조회
@api_view(['GET'])
def home(request, date):
    try:
        # 해당 날짜의 모든 Record 인스턴스를 조회
        records = Record.objects.filter(created_at=date)
        record_serializer = RecordSerializer(records, many=True)

        # 해당 날짜의 모든 News 인스턴스를 조회
        news_serializer = calNews(request, date)
  
        # 결과를 합쳐서 반환
        response_data = {
            'records': record_serializer.data,
            'news': news_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)