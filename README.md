# Webtoon_Crawler_Django

```
from webtoon.models import *

# webtoon_id가 702608인 웹툰의 인스턴스를 생성합니다.
w = Webtoon.objects.create(webtoon_id='702608')
# get_webtoon()으로 웹툰의 이름, 작가, 설명을 불러옵니다.
w.get_webtoon()
# get_episode_list()으로 해당 웹툰의 리스트를 불러옵니다.
w.get_episode_list()
# 불러온 정보를 저장합니다
w.save()
```

