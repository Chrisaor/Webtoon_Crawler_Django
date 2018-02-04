from django.db import models

# Create your models here.

class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}({self.webtoon_id})'

class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=200)
    episode_title = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    created_date = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.webtoon}, 제목: {self.episode_title}, 별점: {self.rating}| 날짜: {self.created_date}'