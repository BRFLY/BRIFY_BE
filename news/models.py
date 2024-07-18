from django.db import models

class News(models.Model):
  title = models.TextField()
  description = models.TextField()
  link = models.TextField()
  pubDate = models.CharField(max_length=10)
  created_at = models.DateField(auto_now_add=True)