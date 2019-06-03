#########################################
# API 요청시 수행하는 작업들을 정의한 패키지 #
#########################################

from datetime import datetime, timedelta, timezone
from dateutil import parser
from time import sleep
import requests
import re

import nlp
import config
import error


# 방송 리스트 요청시 수행되는 함수
# 유튜브 DATA API로부터 현재 생방송 중인 방송 리스트를 가져옴
def get_live_list():
    
    # 유튜브 DATA API에 접근하기 위한 URL 생성
    # key: API 키
    # part: API 응답 중 가져올 부분을 정의
    # fields: 가져올 부분을 상세하게 정의
    # playlistId: 생방송 목록이 저장된 플레이리스트 ID
    # maxResults: 한 번에 가져올 결과의 개수
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    url += '?key=' + config.API_CONFIG['key']
    url += '&part=snippet'
    url += '&fields=items/snippet(title,resourceId/videoId,thumbnails/medium/url)'
    url += '&playlistId=PLU12uITxBEPGpEPrYAxJvNDP6Ugx2jmUx'
    url += '&maxResults=50'
    
    # HTTP Get 요청 후 결과를 JSON으로 파싱
    while True:
        result = requests.get(url).json()
        # Youtube API에 문제가 있다면 딜레이 후 다시 요청
        if 'error' not in result:
            break
        else:
            sleep(1)

    # 정상적으로 응답을 받아오면 응답 메세지 작성
    # {"items": [{
    #         "title": "방송 제목",
    #         "videoId": "방송 ID",
    #         "thumbnail": "썸네일 url",
    #     }, ...
    # ]}
    
    first = True
    response = '{"items":['
    for item in result['items']:
        title = item['snippet']['title']
        # double quote가 문자열에 있으면 JSON을 작성할 떄 문제를 야기하므로
        # single quote로 교체
        # 그 외 인코딩 에러를 일으키는 특수문자들 제거
        title = title.replace('\"', '\'')
        title = title.replace('\\', '')
        title = title.replace('\n', '')
        # 안드로이드 이모지는 utf-8 인코딩 시에 문제를 일으키므로 제거
        title = title.replace('\ud83d', '')
        title = title.replace('\ude04', '')
        title = title.replace('\ud30a', '')
        title = title.replace('\ude03', '')
        title = title.replace('\u263a', '')
        title = title.replace('\ude09', '')
        video_id = item['snippet']['resourceId']['videoId']
        if 'thumbnails' in item['snippet']:
            thumbnail = item['snippet']['thumbnails']['medium']['url']
            
        # 생방송이 외부 접근을 차단하여 썸네일을 반환해주지 못할 경우 처리
        else:
            thumbnail = "/private.jpg"
        if first is True:
            first = False
            response += '{"title":"' + title + '"'
            response += ',"video_id":"' + video_id + '"'
            response += ',"thumbnail":"' + thumbnail + '"}'
        else:
            response += ',{"title":"' + title + '"'
            response += ',"video_id":"' + video_id + '"'
            response += ',"thumbnail":"' + thumbnail + '"}'
    response += ']}'
    return response


# 방송 정보 요청시 수행되는 함수
# 유튜브 DATA API로부터 파라메터로 받은 생방송의 정보를 가져옴
def get_live_info(param):
    
    # 파라메터가 videoId가 아니면 익셉션 발생
    if 'videoId' not in param:
        raise error.InvalidParameterError
        
    # 유튜브 DATA API에 접근하기 위한 URL 생성
    # key: 유튜브 API 키
    # part: API 응답 중 가져올 부분을 정의
    # fields: 가져올 부분을 상세하게 정의
    # id: 정보를 가져올 방송의 ID 값
    url = 'https://www.googleapis.com/youtube/v3/videos'
    url += '?key=' + config.API_CONFIG['key']
    url += '&part=liveStreamingDetails'
    url += '&fields=items/liveStreamingDetails(activeLiveChatId,concurrentViewers)'
    url += '&id=' + param['videoId'][0]
    
    # HTTP Get 요청 후 결과를 JSON으로 파싱
    while True:
        result = requests.get(url).json()
        # Youtube API에 문제가 있다면 딜레이 후 다시 요청
        if 'error' not in result:
            break
        else:
            sleep(1)
        
    # 정상적으로 응답을 받아오면 응답 메세지 작성
    # {
    #     "chatId": "채팅의 ID",
    #     "viewers": "현재 시청자 수"
    # }
    chat_id = result['items'][0]['liveStreamingDetails']['activeLiveChatId']
    viewers = result['items'][0]['liveStreamingDetails']['concurrentViewers']
    response = '{"chatId": "' + chat_id + '",'
    response += '"viewers": "' + viewers + '"}'
    return response


# 채팅 정보 요청시 수행되는 함수
# 유튜브 DATA API로부터 채팅 내용을 가져옴
def get_chat(param):
    
    # chatId를 파라메터로 받지 못헀다면 익셉션 발생
    if 'chatId' not in param:
        raise error.InvalidParameterError
        
    # 유튜브 DATA API를 요청하기 위한 URL 생성
    # key: 유튜브 API 키
    # part: API 응답 중 가져올 부분을 정의
    # fields: 가져올 부분을 상세하게 정의
    # liveChatId: 채팅 내용을 요청하기 위한 ID
    # pageToken: 채팅 내용 중복을 막기 위한 offset
    url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    url += '?key=' + config.API_CONFIG['key']
    url += '&part=snippet'
    url += '&fields=items/snippet(publishedAt,displayMessage),nextPageToken'
    url += '&liveChatId=' + param['chatId'][0]
    if 'pageToken' in param:
        url += '&pageToken=' + param['pageToken'][0]
    
    # HTTP Get 요청 후 결과를 JSON으로 파싱
    while True:
        result = requests.get(url).json()
        # Youtube API에 문제가 있다면 딜레이 후 다시 요청
        if 'error' not in result:
            break
        else:
            sleep(1)

    # 정상적으로 응답을 받아오면 응답 메세지 작성
    # {
    #     "nextPageToken": "다음 페이지 토큰",
    #     "items": [
    #         {
    #             "timestamp": "채팅 메세지가 작성된 시각",
    #             "message": "채팅의 내용"
    #         }, ...
    #     }],
    #     "ranks": ["키워드", "탑", "3"]
    # }
    first = True
    
    # 채팅 키워드 분석을 위한 말뭉치 객체
    corpus = ''
    now = datetime.now(tz=timezone.utc)
    response = '{"nextPageToken":"' + result['nextPageToken'] + '"'
    
    # 채팅이 하나도 없을 경우 처리
    if len(result['items']) == 0:
        response += ''
    else:
        response += ',"items":['
        for item in result['items']:
            timestamp = item['snippet']['publishedAt']
            if (now - timedelta(seconds=10)) < parser.parse(timestamp):
                
                # 채팅 메세지 중 "나 \가 있으면 JSON 작성 시 문제가 발생하는 문제 처리
                message = item['snippet']['displayMessage']
                message = message.replace('\"', '\'')
                message = message.replace('\\', '')
                # 안드로이드 이모지는 utf-8 인코딩 시에 문제를 일으키므로 제거
                message = message.replace('\ud83d', '')
                message = message.replace('\ude04', '')
                message = message.replace('\ud30a', '')
                message = message.replace('\ude03', '')
                message = message.replace('\u263a', '')
                message = message.replace('\ude09', '')

                # 말뭉치에 채팅 내용 추가
                corpus += message + ' '
                if first is True:
                    first = False
                    response += '{"timestamp":"' + timestamp + '"'
                    response += ',"message":"' + message + '"}'
                else:
                    response += ',{"timestamp":"' + timestamp + '"'
                    response += ',"message":"' + message + '"}'
        response += ']'
        
        # 채팅 메세지의 키워드 분석
        # 의미 없는 특수문자들을 제거함
        corpus = re.sub('''[!@#$%^&*()-_=+\|'",./?~]''', ' ', corpus)
        
        # 띄어쓰기 수정
        corrected_corpus = nlp.spacing_check(corpus)
        
        # 키워드 상위 3개를 추출함
        ranks = nlp.get_word_rank(corrected_corpus)
        
        # 마땅한 키워드가 없을 경우 처리
        if len(ranks) == 0:
            response += ''
        else:
            first = True
            response += ',"ranks":['
            for r in ranks:
                if first is True:
                    first = False
                    response += '"' + r + '"'
                else:
                    response += ',"' + r + '"'
            response += ']'
    response += '}'
    return response
