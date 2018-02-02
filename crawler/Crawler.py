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


