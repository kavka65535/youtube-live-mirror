##############################
# HTTP 요청 핸들러 재정의 클래스 #
##############################

import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

import error
import api_process


# HTTP 요청 핸들러 상속
class RequestHandler(BaseHTTPRequestHandler):

    # 페이지 요청시 반환할 성공 헤더
    def _send_www_success(self):
        self.send_response(200, 'Success')
        # 응답이 text/html임을 명시
        self.send_header('Content-Type', 'text/html charset=UTF-8')
        self.end_headers()

    # API 요청시 반환할 성공 헤더
    def _send_api_success(self):
        self.send_response(200, 'Success')
        # 응답이 json임을 명시
        self.send_header('Content-Type', 'application/json charset=UTF-8')
        self.end_headers()
        
    # 이미지 파일 요청시 반환할 성공 헤더
    def _send_img_success(self):
        self.send_response(200, 'Success')
        # 응답이 file 타입 이미지임을 명시
        self.send_header('Content-Type', 'image/jpeg')
        self.end_headers()

    # Get 요청 핸들러 재정의
    def do_GET(self):
        try:
            # 요청 url 경로를 파싱함
            parsed = urlparse(self.path)
            
            # favicon.ico 요청 무시
            if '/favicon.ico' == parsed.path:
                return
            
            # 외부 접근 차단 영상 썸네일 이미지 반환
            elif '/private.jpg' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'static', 'private.jpg'), 'rb')
                self._send_img_success()
                self.wfile.write(f.read())
                f.close()
                
            # 전체 키워드 1, 2, 3순위 아이콘 이미지 반환
            elif '/1.png' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'static', '1.png'), 'rb')
                self._send_img_success()
                self.wfile.write(f.read())
                f.close()
            elif '/2.png' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'static', '2.png'), 'rb')
                self._send_img_success()
                self.wfile.write(f.read())
                f.close()
            elif '/3.png' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'static', '3.png'), 'rb')
                self._send_img_success()
                self.wfile.write(f.read())
                f.close()
            
            # root 요청시 index.html 반환
            # 프로젝트 내 경로에 있는 파일을 읽어 응답 메세지에 작성
            elif '/' == parsed.path:
                # 파일을 바이너리 모드로 읽어 작성
                f = open(os.path.join(os.getcwd(), 'www', 'index.html'), 'rb')
                self._send_www_success()
                self.wfile.write(f.read())
                f.close()
                
            # view.html 페이지
            # 옵션 형식: ?v=blabla123
            elif '/view.html' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'view.html'), 'rb')
                self._send_www_success()
                self.wfile.write(f.read())
                f.close()
                
            # Javascript 함수 로드
            elif '/js/function.js' == parsed.path:
                f = open(os.path.join(os.getcwd(), 'www', 'js', 'function.js'), 'rb')
                self._send_www_success()
                self.wfile.write(f.read())
                f.close()

            # 유튜브 방송 리스트 API 요청
            elif '/api/list' == parsed.path:
                response = api_process.get_live_list()
                self._send_api_success()
                self.end_headers()
                # utf-8 형식의 string을 byte array로 인코딩
                self.wfile.write(response.encode('utf-8'))

            # 유튜브 라이브 방송 정보 API 요청
            # 동영상 ID를 통해 방송 정보를 반환
            # 옵션
            # videoId: 유튜브 영상 ID
            elif '/api/liveInfo' == parsed.path:
                # 옵션 쿼리 파싱
                param = parse_qs(parsed.query)
                # ID를 통해 가져온 방송 정보를 JSON 형식으로 작성
                response = api_process.get_live_info(param)
                self._send_api_success()
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))

            # 유튜브 라이브 방송의 채팅 메세지 API 요청
            # 라이브 방송의 채팅 ID를 통해 채팅 채팅메세지 배열을 반환
            # 옵션
            # chatId: 라이브방송 채팅 ID
            # nextPageToken: 채팅의 반환이 중복되는 것을 막기 위한 offset
            elif '/api/chat' == parsed.path:
                param = parse_qs(parsed.query)
                response = api_process.get_chat(param)
                self._send_api_success()
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                
            # 정의된 경로 이외의 접근이라면 Invalid Url Error 익셉션을 발생시킴
            else:
                raise error.InvalidUrlError
        
        # 정의된 경로 이외의 접근시 HTML 상태코드 400 반환
        except error.InvalidUrlError as e:
            print(e, file=sys.stderr)
            self.send_error(400, 'Invalid Url')
            
        # 옵션 파라메터의 형식이나 값이 잘못됬을 경우 상태코드 400 반환
        except error.InvalidParameterError as e:
            print(e, file=sys.stderr)
            self.send_error(400, 'Invalid Parameter')
        
        # Youtube API 서버에 문제가 있어 응답을 할 수 없는 경우 상태코드 400 반환
        except error.APIUnavailableError as e:
            print(e, file=sys.stderr)
            self.send_error(400, e)
            
        except Exception as e:
            print(e, file=sys.stderr)
            self.send_error(400, e)
            
