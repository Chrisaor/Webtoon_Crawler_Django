import re
import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from webtoon.models import Webtoon, Episode


# utils가 있는 위치
PATH_MODULE = os.path.abspath(__file__)
# project container(crawler폴더)의 위치
ROOT_DIR = os.path.dirname(PATH_MODULE)
# data/ 폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class WebtoonC:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.webtoon_name = None
        self.author = None
        self.description = None

    def get_webtoon_info(self, refresh_html=False):

        '''
        웹툰 페이지를 data/webtoon.html 위치에 저장
        :param refresh_html: True일 경우, 무조건 새 HTML파일을 사이트에서 받아와 덮어씀
        Q1: 어디서 인수를 받아오는 건지(?)
        :return:
        '''
        # 만약에 path_data_dir에 해당하는 폴더가 없을 경우 생성해줌
        os.makedirs(DATA_DIR, exist_ok=True)

        # webtoon.html 경로
        FILE_PATH = os.path.join(DATA_DIR, f'webtoon_{self.webtoon_id}.html')

        # 웹툰 페이지 HTML을 FILE_PATH[data/webtoon.html]에 저장
        try:
            # refresh_html매개변수가 True일 경우, wt모드로 파일을 열어 새로 파일을 다운받도록 함
            # False라면 xt모드(파일이 존제하지 않을 경우에만 쓰기)
            file_mode = 'wt' if refresh_html else 'xt'
            with open(FILE_PATH, file_mode, encoding='utf8') as f:
                # 웹툰 주소
                url_webtoon = 'https://comic.naver.com/webtoon/list.nhn?'
                params = {
                    'titleId' : self.webtoon_id,
                }

                response = requests.get(url_webtoon, params)
                source = response.text
                f.write(source)
            # xt모드에서 있는 파일을 열려고 한 경우 발생하는 예외
        except FileExistsError:
            print(f'"{FILE_PATH}" file is already exists!')

            # webtoon.html을 읽고 source에 할당
        source = open(FILE_PATH, 'rt', encoding='utf8').read()
        # soup 변수에 BeautifulSoup클래스 호출에 source를 전달해 만들어진 인스턴스를 할당
        # Q2: soup변수에 인스턴스를 할당? soup이라는 인스턴스를 생성?
        soup = BeautifulSoup(source, 'lxml')
        # BeautifulSoup을 사용해 HTML을 탐색하며 dict의 리스트를 생성,

        # 가져올 정보를 담을 결과 dict
        result = dict()

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
        # webtoon.html 경로
        FILE_PATH = os.path.join(DATA_DIR, f'webtoon_{self.webtoon_id}.html')
        # source에 webtoon.html을 읽고 할당
        source = open(FILE_PATH, 'rt', encoding='utf8').read()
        # BeautifulSoup 인스턴스 생성
        soup = BeautifulSoup(source, 'lxml')
        # 모든 TR를 찾아라! -> list
        find_tr = soup.find_all('tr')[2:]
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
    # get_webtoon = WebtoonC(703835)
    get_webtoon = WebtoonC(699659)

    webtoon_info_dict = get_webtoon.get_webtoon_info()
    wt_instance = Webtoon(webtoon_id=webtoon_info_dict['webtoon_id'], webtoon_name=webtoon_info_dict['webtoon_name'],
            author=webtoon_info_dict['author'], description=webtoon_info_dict['description'])
    wt_instance.save()

    episode_list = get_webtoon.get_episode_list()
    for i in episode_list:
        wt_instance.episode_set.create(episode_title=i['episode_title'], rating=i['rating'], created_date=i['created_date']).save()
