/********************************/
/* Javascript 함수를 정의한 패키지 */
/********************************/

/* URL로부터 파라메터를 추출하는 함수 */
// 페이지 이동 시 서버를 거치지 않기 때문에 파라메터 전송을 위해
// get 방식으로 데이터를 url에 작성하고 이를 파싱해서 사용하도록 함
function getQueryString() {
    /* 파라메터를 쿼리 형식을 표현하는데 사용하는 문자들로 잘라 값 추출 */
    var params = window.location.search.substr(1).split('&');
    if (params == "") return {};
    var param = {};
    for (var i = 0; i < params.length; ++i) {
        var p = params[i].split('=', 2);
        if (p.length == 1)
            param[p[0]] = "";
        else
            param[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return param;
}

/* 파라메터를 받아 차트의 내용을 업데이트하는 함수 */
function updateChart(chart, label, viewers, chats) {
    /* 차트 데이터를 담고있는 큐에 새로운 데이터 푸시 */
    // 차트가 업데이트 될 때마다 조금씩 이동하도록 하기 위해
    // 비어있는 큐를 선언하여 아직 데이터가 들어오지 않았으면
    // 빈 값을 보이게 했기 때문에 푸시만 하면 큐의 크기가 점점 늘어남
    // 그러므로 푸시와 동시에 가장 오래된 데이터를 팝
    chart.data.labels.shift();
    chart.data.labels.push(label);
    chart.data.datasets[0].data.shift();
    chart.data.datasets[0].data.push(viewers);
    chart.data.datasets[1].data.shift();
    chart.data.datasets[1].data.push(chats);
    
    /* 차트 변경 사항들을 업데이트 */
    chart.update();
}

/* 파라메터를 받아 채팅 표시 영역을 업데이트하는 함수 */
function writeChat(chatArea, timestamp, message) {
    var ul = chatArea.getElementsByTagName('ul')[0];
    
    /* 채팅의 양이 너무 많아지면 메모리 스택이 다 차서 */
    /* 오류가 발생하는 것을 방지하여 채팅을 50개만 표시 */
    if (ul.getElementsByTagName('li').length > 50){
        ul.removeChild(ul.childNodes[0]);
    }
    
    /* ul 요소를 불러와 li 차일드 노드를 추가 */
    var chat = document.createElement('li');
    
    /* (작성시각): 채팅 내용 */
    chat.appendChild(document.createTextNode('(' + timestamp + '): ' + message));
    ul.appendChild(chat);
    
    /* 항상 가장 아래쪽으로 스크롤이 가 있도록 함 */
    chatArea.scrollTop = ul.scrollHeight;
}

/* 전체 키워드 순위를 내는 함수 */
function getTotalRank(ranks) {
    var d = {};
    /* 10초간 키워드 탑3를 저장해둔 배열에서 키워드를 키, 등장 횟수를 값으로 딕셔너리 생성 */
    for (var i = ranks.length - 1; i >= 0; i--){
        if (ranks[i]) {
            for (var j = 0; j < 3; j++){
                if (ranks[i][j]){
                    if (d[ranks[i][j]]){
                        d[ranks[i][j]] += 1;
                    }
                    else {
                        d[ranks[i][j]] = 1;
                    }
                }
            }
        }
    }
    /* 딕셔너리를 값을 기준으로 정렬함 */
    // 딕셔너리는 순서가 없으므로 배열로 만들어주고
    // 2차배열의 2번째 요소인 단어의 등장 횟수를 기준으로 정렬해줌
    var k = [];
    var v = [];

    var r = Object.keys(d).map(function(k) {
        return [k, d[k]];
    });
    r.sort(function(a, b) {
        return b[1] - a[1];
    });
    return r;
}