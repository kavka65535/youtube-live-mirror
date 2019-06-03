Youtube Live Mirror
===================

## 개요
유튜브 라이브 방송을 실시간으로 모니터링하고 채팅을 분석한 결과를 함께 보여주는 웹페이지입니다.
현재 방송되고 있는 유튜브 라이브 방송을 시청하면서 실시간으로 변화하는 시청자의 수와 채팅의 양을 차트를 통해 확인할 수 있고, 
채팅의 내용을 분석하여 어떤 단어가 가장 많이 등장하는지에 대한 정보를 제공합니다.
이를 통해 어떤 주제나 키워드가 어느 정도의 관심을 받고 있는지 한 눈에 확인할 수 있습니다.

API서버는 pure python, 웹페이지는 javascript로 구현되어 AJAX를 통해 상호간에 통신합니다.

github에는 보안상 google api key를 올릴 수 없어 config.py의 값이 비어있습니다. 참고 바랍니다.

## 설치
    $ ./requirements.sh
    $ python3 run_server.py
    
혹은

    $ pip3 install requests
    $ python3 run_server.py
    
## 추가
Natural Language Processing에 관한 부연설명은 [여기](https://docs.google.com/presentation/d/e/2PACX-1vR1D1OyYEBICoiT7_oB0XrusLUV0JZ4NU_40TQWs20P-gv_GUZm70uutLov69c6flqrWzfHXt6GB4zn/pub?start=true&loop=false&delayms=3000)에 나와있습니다.
