import re
import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from webtoon.models import Webtoon

class WebtoonC:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.webtoon_name = None
        self.author = None
        self.description = None

    def get_webtoon_info(self):

        url_webtoon = 'https://comic.naver.com/webtoon/list.nhn?'
        params = {
            'titleId' : self.webtoon_id,
        }
        response = requests.get(url_webtoon, params)
        source = response.text
        # soup 변수에 BeautifulSoup클래스 호출에 source를 전달해 만들어진 인스턴스를 할당
        # Q2: soup변수에 인스턴스를 할당? soup이라는 인스턴스를 생성?
        soup = BeautifulSoup(source, 'lxml')
        # BeautifulSoup을 사용해 HTML을 탐색하며 dict의 리스트를 생성,

        # 가져올 정보를 담을 결과 dict

        # 가져올 정보
        # 1. 웹툰이름, 2. 작가, 3. 웹툰 설명 4. 제목, 별점, 등록일 리스트

        # 1. 웹툰이름 찾기!
        # a) source를 받아 생성된 soup객체에서 <div>의 comicinfo클래스 찾음
        DIV_COMIC_INFO = soup.find('div', class_='comicinfo')
        # b) 위의 결과에서 <div>의 detail클래스를 찾은 결과를 prettify메소드를 사용하여 파싱
        # prettify()메소드는 Beautiful Soup parse tree를 잘 정돈된 '스트링'으로 반환함
        DIV_COMIC_DETAIL = DIV_COMIC_INFO.find('div', class_='detail').prettify()
        # c) 제목의 정확한 위치를 정규표현식으로 찾음. 이상하게 찾았음(추후 수정)
        PATTERN_FIND_WEBTOON_NAME = re.compile(r'<h2>\s+?\W\W(.*?)\s+?<span', re.S)
        webtoon_name = re.search(PATTERN_FIND_WEBTOON_NAME, DIV_COMIC_DETAIL).group(1)
        # 2. 작가 찾기
        # a) 위 DIV_COMIC_INFO를 가져와서 <span>의 'wrt_nm'클래스를 찾는다
        SPAN_WRT_NM = DIV_COMIC_INFO.find('span', class_='wrt_nm')
        # b) <span> 안쪽의 텍스트만 가져온다. 공백은 제거하고(strip=True)
        author = SPAN_WRT_NM.get_text(strip=True)
        # 3. 웹툰 설명
        # a) 역시 DIV_COMIC_INFO를 가져와서 <p>를 가져온다
        description = DIV_COMIC_INFO.find('p').get_text(" ")
        # 결과들을 result 리스트에 추가

        result= {
            'webtoon_id' : self.webtoon_id,
            'webtoon_name': webtoon_name,
            'author': author,
            'description': description,
        }

        # print(f'웹툰 이름 : {webtoon_name} | 작가 : {author} | 설명 : {description}')

        return result

    def get_episode_list(self):
        # 에피소드의 제목, 별점, 등록일 찾아서 리스트로 나열하기

        # BeautifulSoup 인스턴스 생성
        url_webtoon = 'https://comic.naver.com/webtoon/list.nhn?'
        params = {
            'titleId': self.webtoon_id,
        }
        response = requests.get(url_webtoon, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')
        # 2번째 TR를 찾기 -> list
        # tr_tag에 클래스가 없는 것을 찾는 걸로 추후 수정
        find_tr = soup.find_all('tr')[2:]
        # find_tr = list()
        # for i in soup.find_all('tr'):
        #     tr_tag = BeautifulSoup(i, 'lxml')
        #     if tr_tag.attrs == None:
        #         find_tr.append(i)
        # 결과를 저장할 list
        result = list()
        #TR리스트에서 하나씩 꺼내어 td안의 내용을 건진다
        for tr_element in find_tr:
            # 에피소드 title가져오기
            episode_title = tr_element.find('td', class_='title').find('a').get_text()
            # 에피소드 별점 가져오기
            rating = tr_element.find('div', class_='rating_type').strong.string
            # 에피소드 날짜 가져오기
            created_date = tr_element.find('td', class_='num').get_text()
            # 결과 저장
            result.append({
                'episode_title' : episode_title,
                'rating' : rating,
                'created_date' : created_date,
            })

        return result

if __name__ == '__main__':
    # get_webtoon에 WebtoonC(웹툰 크롤러) 인스턴스를 생성

    get_webtoon = WebtoonC(686669)
    # 웹툰 정보를 가져올 딕셔너리 생성
    webtoon_info_dict = get_webtoon.get_webtoon_info()
    # 웹툰 정보가 담겨있는 딕셔너리를 인수로 넣고 Webtoon모델의 인스턴스를 생성
    wt_instance = Webtoon(webtoon_id=webtoon_info_dict['webtoon_id'], webtoon_name=webtoon_info_dict['webtoon_name'],
            author=webtoon_info_dict['author'], description=webtoon_info_dict['description'])
    # Webtoon모델 인스턴스 저장
    wt_instance.save()
    # 에피소드 리스트 생성
    episode_list = get_webtoon.get_episode_list()
    # 에피소드 리스트의 원소인 딕셔너리를 인스턴스.episode_set.create 인수로 넣고 에피소드를 생성함.
    for i in episode_list:
        wt_instance.episode_set.create(episode_title=i['episode_title'], rating=i['rating'], created_date=i['created_date']).save()
