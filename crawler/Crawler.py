import os
import requests


# utils가 있는 위치
PATH_MODULE = os.path.abspath(__file__)
# project container(crawler폴더)의 위치
ROOT_DIR = os.path.dirname(PATH_MODULE)
# data/ 폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')
# webtoon.html 경로
FILE_PATH = os.path.join(DATA_DIR, 'webtoon.html')

def get_webtoon_info(refresh_html=False):
    '''
    웹툰 페이지를 data/webtoon.html 위치에 저장
    :param refresh_html: True일 경우, 무조건 새 HTML파일을 사이트에서 받아와 덮어씀
    Q1: 어디서 인수를 받아오는 건지(?)
    :return:
    '''
    # 만약에 path_data_dir에 해당하는 폴더가 없을 경우 생성해줌
    os.makedirs(DATA_DIR, exist_ok=True)

    # 웹툰 주소
    url_webtoon = 'https://comic.naver.com/webtoon/list.nhn?titleId=703835'

    # 웹툰 페이지 HTML을 FILE_PATH[data/webtoon.html]에 저장
    try:
        # refresh_html매개변수가 True일 경우, wt모드로 파일을 열어 새로 파일을 다운받도록 함
        # False라면 xt모드(파일이 존제하지 않을 경우에만 쓰기)
        file_mode = 'wt' if refresh_html else 'xt'
        with open(FILE_PATH, file_mode, encoding='utf8') as f:
            response = requests.get(url_webtoon)
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

    # 가져올 정보를 담을 결과 리스트
    result = []

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
