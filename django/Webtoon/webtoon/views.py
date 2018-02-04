from django.http import HttpResponse
from django.shortcuts import render
from webtoon.models import Webtoon, Episode


def index(request):
    webtoon_list = Webtoon.objects.all()
    context = {
        'webtoon_list' : webtoon_list,
    }
    return render(request, 'webtoon/index.html', context)

def detail(request, webtoon_id):
    webtoon = Webtoon.objects.get(pk=webtoon_id)
    context = {
        'webtoon' : webtoon,
        'episode_list' : Episode.objects.filter(webtoon=webtoon)
    }
    # return HttpResponse('You are looking at webtoon %s' % webtoon_id)
    return render(request, 'webtoon/detail.html', context)