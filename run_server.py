###############################
# HTTP 서비스를 실행하는 스크립트 #
###############################

import os
import sys
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from http.server import HTTPServer
from request_handler import RequestHandler


def main():
    
    # 서버 설정
    # HTTPS/443번 포트로 서비스 실행
    # 모든 IP로부터의 접근 허용
    PORT = 443
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)

    # 로그 파일 이름으로 현재 날짜 사용
    kst = timezone(timedelta(hours=9))
    now = datetime.now(tz=kst).strftime('%Y%m%d')
    
    # 표준에러를 지정된 파일로 열어 로그 기록
    sys.stderr = open('./log/{}.log'.format(now), 'a', 1)

    # 서버 실행
    print("Started WebServer on port {}...".format(PORT))
    print("Press ^C to quit")
    server.serve_forever()


if __name__ == '__main__':
    main()
