import os
import urllib.request 
import json
from datetime import datetime
from rest_framework.decorators import api_view

from news.models import News
from news.serializers import NewsSerializer
from rest_framework.response import Response


def getNaverSearchData(srcText, cnt): # srcText : 검색어
    base = "https://openapi.naver.com/v1/search/news"
    parameters = "?query=%s&display=%s&sort=%s" % (urllib.parse.quote(srcText), cnt, "sim") #20개씩 가져오기

    url = base + parameters
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", "ODB7QKol8n7V9PGTymy7")
    req.add_header("X-Naver-Client-Secret", "a3AKwO6aRU")

    response = urllib.request.urlopen(req)
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8')).get('items')

# 오늘 날짜인지 확인하고, news 객체에 저장
def filterData(item): 
    pubDate = datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
    pDate = pubDate.date()
    today = datetime.now().date()

    if pubDate == today:
        news = News(
          title = item['title'],
          description = item['description'],
          link = item['link'],
          pubDate = pDate
        )
        news.save()
        return 

# 캘린더 페이지
@api_view(['GET'])
def calNews(request, date):
    # 오늘 뉴스가 존재하는지 확인 -> 있으면 오늘 뉴스 반환하는 함수로 보내기
    input_date = datetime.strptime(date, '%Y-%m-%d').date()
    pastNews = News.objects.filter(created_at=input_date)
    if not pastNews.exists():
        # 오늘 뉴스가 없는 경우 : 최초 생성
        # 검색 결과 - JSON 배열
        items = getNaverSearchData("경제", 20)
        for item in items: filterData(item)
        items = getNaverSearchData("사회", 20)
        for item in items: filterData(item)
        items = getNaverSearchData("취준", 20)
        for item in items: filterData(item)

        pastNews = News.objects.filter(created_at=input_date)

    serializer = NewsSerializer(pastNews, many=True)
    return serializer.data

# 뉴스 페이지에서 요청하는 건에 대한 response
@api_view(['GET'])
def forNews(request):
    
    eco_items = getNaverSearchData("경제", 4)
    soc_items = getNaverSearchData("사회", 4)
    job_items = getNaverSearchData("취준", 4)
    
    response_data = {
        'eco_news': eco_items,
        'soc_news': soc_items,
        'job_news': job_items,
    }
    return Response(response_data)