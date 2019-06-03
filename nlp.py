#####################################
# 자연어 처리 관련 함수들을 정의한 패키지 #
#####################################

import requests


# 띄어쓰기를 수정하는 함수
# 네이버 띄어쓰기 검사기를 사용
def spacing_check(corpus):
    
    # 네이버 띄어쓰기 검사기 요청 URL
    url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy'
    
    # 옵션
    # q: 검사할 문장
    # color_blindness: 색약을 위한 옵션
    params = {
        'q': corpus,
        'color_blindness': 0
    }
    
    # HTTP Get 요청 후 json으로 파싱
    result = requests.get(url, params=params).json()
    
    # 띄어쓰기 검사 결과 string 반환
    return result['message']['result']['notag_html']


# 문장에서 키워드를 추출하는 함수
# 이 부분에 대한 자세한 설명은 PPT로 대체
# README.md를 참고해주세요
def get_word_rank(corpus):
    count = {}
    # 말뭉치를 띄어쓰기별로 자르고 
    for word in corpus.split():
        # 이를 다시 왼쪽부터 한 글자씩 잘라 토큰화하여 저장
        # key: 토큰, value: 등장 횟수
        for e in range(1, len(word)+1):
            if not count.get(word[:e]):
                count[word[:e]] = 1
            else:
                count[word[:e]] += 1
    # 토큰의 등장 횟수에 따라 정렬
    items = sorted(count.items(), key=lambda x: x[1], reverse=True)
    rank = [] # 추출된 키워드를 횟수가 많은 순으로 저장할 배열
    temp = '' # 토큰 값을 임시로 저장할 스트링
    # 등장 횟수가 많은 것부터 단어 추출
    for token, _ in items:
        # 의미를 알기 힘든 길이가 1인 토큰은 패스
        if len(token) < 2: 
            continue
        # 새로운 토큰이 이전 토큰을 포함하고 있다면 단어일 가능성이 높음    
        if temp in token: 
            temp = token
        # 새로운 토큰이 다른 단어로 변했다면 직전 토큰을 반환
        elif temp not in token:
            rank.append(temp)
            temp = token
    # 상위 세개의 단어만 리턴
    if len(rank) > 3:
        return rank[:3]
    else:
        return rank
