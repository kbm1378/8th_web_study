'''
웹 스크래핑 (requests, BeautifulSoup4)
- 웹스크래핑은 왜 필요할까요?
    - Open API를 제공하지 않는 데이터를 가져올 때 필요합니다. (https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303)
    - 반대로, Open API가 제공되고 있다면 굳이 필요없습니다. (http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/bikeList/1/99)
    - 즉, Open API여부를 먼저 확인하고 없을 경우만!
    - 수집해보고 싶은 데이터가 있었거나, 단순 반복 스크랩 업무를 하고 있었다면 정말 유용합니다. (하지만 웹개발에서 필수는 아닙니다.)
    - 이를 위해 requests와 BeautifulSoup4 이라는 패키지를 사용합니다.
- 파이썬 패키지 & 가상환경
    - 패키지 : 유용한 기능들을 Python으로 미리 구현해둔 것
    - pip 을 통해 설치 (pip : 파이썬 세계의 앱스토어) (ex: pip install requests)
    - 가상환경 : 한 컴퓨터에서 여러 프로젝트에 사용되는 서로다른 패키지/버젼을 관리하기 위한 개념
- Requests & BeautifulSoup4
    - 웹 스크래핑에 사용되는 파이썬 패키지
    - 사용 패턴이 단순하므로 실습/숙제 코드만 잘 정리해두시면 됩니다!
    - (좀 더 관심있으시다면? 셀레니움, 퍼펫티어)

DB (MongoDB, pymongo)
- DB란?
    - 사용될 목적으로 저장/관리 되는 데이터의 집합
    - DB의 2가지 종류 : RDBMS (엑셀), No-SQL (딕셔너리)
    - 변경될 여지가 없는 경우 → RDBMS, 변경 및 확장될 가능성이 높은 경우 → No-SQL / 처음 개발하는 관점에서 더 효과적인 것은 No-SQL!
- MongoDB란?
    - No-SQL 개념 DB 중 1개 (그 외에도 Redis, HBase 등 다양해요!) (https://namu.wiki/w/NoSQL)
    - (RDBMS의 경우 MySQL, PostgreSQL 등이 있습니다.)
    - 구조는 db (엑셀 "파일"에 대응)와 collection ("시트"에 대응)으로 구성.
    - 즉, 특정 서비스를 db로 그 서비스 내의 다양한 정보 종류를 collection으로 구분
- pymongo
    - MongoDB 관리에 사용되는 파이썬 패키지
    - 사용 패턴이 단순하므로 요약 코드들만 잘 정리해두시면 됩니다!
'''

# 설치한 패키지 (requests, BeautifulSoup4, pymongo 등)를 사용하기 위해 import 필요
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# 본인 컴퓨터에 설치한 MongoDB에 접속하는 과정
client = MongoClient('localhost', 27017)
# MongoDB에 "dbsparta"라는 이름의 DB를 없다면 생성 후 접속/있다면 접속하는 과정
db = client.dbsparta

# 지니 음악 사이트 랭킹 페이지 정보를 가져오는 과정
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 위 부분은 왜 필요할까요? -> 일부 웹사이트는 스크래핑을 막기 위해 비정상적 접속인 경우 차단하는 경우가 있음. 
# 이와 관련하여 이 요청이 일반적인 브라우저에서의 요청인 것처럼 하는 것. 
# (크롬으로 사이트 들어가서 개발자 도구 > Network > Request Headers > User Agent 보기)
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200309', headers=headers)
# 해당 정보를 BeautifulSoup을 통해 스크래핑하기 쉽도록 정제하는 과정
soup = BeautifulSoup(data.text, 'html.parser')
# 음원 정보가 담긴 tr 태 리스트를 추출하는 코드 (크롬 개발자 도구를 통해 구조 파악 후 진행)
musics = soup.select('div.newest-list > div.music-list-wrap > table > tbody > tr')

for music in musics:
    rank_tag = music.select_one('td.number')
    title_tag = music.select_one('td.info > a.title')
    artist_tag = music.select_one('td.info > a.artist')
    if title_tag is not None and artist_tag is not None:
        # strip : 문자열에서 공백 제거하는 함수
        title = title_tag.text.strip()
        artist = artist_tag.text.strip()

        # rank의 경우 콘텐츠 텍스트 외에도 내부에 tag가 있어 꺼내는 데에 약간 어려움이 있습니다. 
        # 1번 방법
        # split 사용하기 : https://wikidocs.net/13#split
        # rank_tag.text 가 리스트로 나온다는 점 -> spl
        rank = rank_tag.text.split()[0]

        # 2번 방법
        # BeautifulSoup 라이브럴리 사용 : https://www.crummy.com/software/BeautifulSoup/bs4/doc/#decompose
        rank_tag.select_one('span.rank').decompose()
        rank = rank_tag.text.strip()
        doc = {
            'rank': rank,
            'title': title,
            'artist': artist
        }
        print(rank, title, artist)
        # DB Insert
        db.musics.insert_one(doc)

# 실행 후 Robo 3T로 확인하기!