from django.db import models


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=200, default='webtoon id' )
    webtoon_name = models.CharField(max_length=200, default='webtoon name')
    author = models.CharField(max_length=200, default='author')
    description = models.CharField(max_length=200, default='description')

    def __str__(self):
        return f'{self.webtoon_name} | {self.author}({self.webtoon_id})'



class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE, blank=True, null=True)
    episode_title = models.CharField(max_length=200, default='title')
    rating = models.CharField(max_length=200, default='rating')
    created_date = models.CharField(max_length=200, default='created_date')

    def __str__(self):
        return f'제목: {self.episode_title} | 별점: {self.rating} | 날짜: {self.created_date}'
