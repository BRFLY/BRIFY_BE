from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class Record(models.Model):
  text = models.TextField()     # 채팅 텍스트

  created_at = models.DateField(default=now) # 날짜 조회 할 때 사용

  def created_time():
    date = datetime.now()
    # 분
    minute = date.strftime("%M")   # 00~23 / 00~59 / string 반환
    # 시
    hour = int(date.strftime("%H"))

    if hour < 12:
      period = "오전"
    else:
      period = "오후"

    # 24시간 형식을 12시간 형식으로 변환 ex. 23시 -> 11시
    hour_12 = hour % 12
    if hour_12 == 0:
      hour_12 = 12  # 0시는 12시로 표시

    created_time = f"{period} {hour_12}:{minute}"   # string 타입이에요.
    return created_time
  
  time = created_time()     # 카톡처럼 채팅 옆에 뜰 시간

  