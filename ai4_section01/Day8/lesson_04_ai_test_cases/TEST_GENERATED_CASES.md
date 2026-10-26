# 계약 기반 테스트표

기대값은 README의 업무 계약과 사용자 계약에서 계산했다.
성공 본문 표기는 `(amount, discount, payable)`이며, 실제 검사는 세 필드의 JSON 객체 전체를 비교한다.
모든 행은 사전 상태가 없고 독립적으로 POST /quotes를 한 번 요청한다.
E(amount)는 비어 있지 않은 detail 배열에 loc=["body", "amount"]인 오류가 있는 본문,
E(body)는 loc=["body"]인 오류가 있는 본문이다. 오류 전문은 계약에 없으므로 고정하지 않는다.
오류 배열과 위치 검사는 제공 test_api.py의 FastAPI 오류 형식을 따른다.

| ID | 입력(JSON) | 사전 상태 | 요청 순서 | 기대 상태 | 기대 본문 | 근거 |
|---|---|---|---|---|---|---|
| N01 | `{"amount":5000}` | 없음 | POST /quotes 1회 | 200 | (5000, 0, 5000) | 정상, 할인 미적용 |
| N02 | `{"amount":20000}` | 없음 | POST /quotes 1회 | 200 | (20000, 1000, 19000) | 정상, 정액 할인 |
| L01 | `{"amount":1}` | 없음 | POST /quotes 1회 | 200 | (1, 0, 1) | 허용 최솟값 |
| L02 | `{"amount":100000}` | 없음 | POST /quotes 1회 | 200 | (100000, 1000, 99000) | 허용 최댓값 |
| R01 | `{"amount":9999}` | 없음 | POST /quotes 1회 | 200 | (9999, 0, 9999) | 할인 경계 직전 |
| R02 | `{"amount":10000}` | 없음 | POST /quotes 1회 | 200 | (10000, 1000, 9000) | 핵심 회귀, 이상에 경계 포함 |
| R03 | `{"amount":10001}` | 없음 | POST /quotes 1회 | 200 | (10001, 1000, 9001) | 할인 경계 직후 |
| B01 | `{"amount":0}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 최솟값 바로 밖 |
| B02 | `{"amount":100001}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 최댓값 바로 밖 |
| M01 | `{}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 필수 필드 누락 |
| M02 | 본문 없음 | 없음 | 본문 없이 POST /quotes 1회 | 422 | E(body) | 필수 본문 누락 |
| T01 | `{"amount":"10000"}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 숫자 문자열 거부 |
| T02 | `{"amount":10000.0}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 정수값의 실수도 거부 |
| T03 | `{"amount":1.5}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 소수 거부 |
| T04 | `{"amount":true}` | 없음 | POST /quotes 1회 | 422 | E(amount) | bool의 정수 취급 방지 |
| T05 | `{"amount":null}` | 없음 | POST /quotes 1회 | 422 | E(amount) | null 불허 |
| T06 | `{"amount":[]}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 배열 불허 |
| T07 | `{"amount":{}}` | 없음 | POST /quotes 1회 | 422 | E(amount) | 객체 불허 |

상태 전이·요청 간 순서 의존·외부 장애는 저장 상태, DB, 외부 API가 없어 제외했다.
인증·자원 충돌은 이번 계약에 없으므로 추가하지 않았다.

## 문서와 구현의 차이

- openapi_snapshot.json은 작업 폴더에서 발견되지 않았다. 저장 스냅샷의 실제 내용은 비교하지 못했다.
- README 업무 계약과 test_api.py는 성공 200을 요구한다. README 경로 요약표의 201 / 422는 업무 계약과 불일치한다.
- main.py의 amount 검증은 strict=True, ge=1, le=100000으로 입력 계약과 일치한다.
- main.py의 할인 조건은 amount > 10000이므로 정확히 10000원에서 계약의 '이상'과 다르다.

## 생성 테스트 자체 검토

- 첫 줄은 from main import app이며 TestClient를 사용한다.
- 표의 18개 ID가 pytest 항목에 연결된다. 각 요청은 독립적이다.
- 기대 본문은 업무 계약에서 손계산한 상수이며 구현의 할인 함수를 호출하지 않는다.
- 성공 상태와 본문 전체를 비교해 필드 누락·추가 및 계산 오류를 검출한다.
- Python에서 bool/float가 int와 같다고 비교될 수 있어 성공 금액 필드의 정수 타입도 확인한다.
- 오류는 422와 제공 테스트의 detail/loc 형식을 검사한다. 구현 버전에 따른 오류 문구 전체는 고정하지 않는다.
- R02에 xfail/skip을 붙이거나 잘못된 실제값을 기대값으로 채택하지 않았다.
- main.py와 제공 test_api.py는 수정하지 않았다.

## 실제 실행

기존 .venv는 Python 3.15 기반이며 실행에 실패했다. 별도 임시 가상환경을 Python 3.12.14로 만들고 requirements.txt의 지정 버전을 설치했다.
아래 명령의 작업 디렉터리는 이 파일이 있는 4차시 폴더이다. PowerShell에서 실행했다.

```powershell
& "$env:TEMP/fastapi-lesson04-contract312/Scripts/python.exe" -m pytest -q test_generated.py
& "$env:TEMP/fastapi-lesson04-contract312/Scripts/python.exe" -m pytest -q test_api.py
```

| 실제 명령 대상 | 실제 결과 | 실패 항목 |
|---|---|---|
| test_generated.py | 1 failed, 17 passed, 1 warning (0.56s) | test_quote_success[R02] |
| test_api.py | 1 failed, 10 passed, 1 warning (0.34s) | test_quote[10000-1000-9000] |

두 실행 모두 종료 코드 1이다. 10000원에서 기대는 discount=1000, payable=9000이지만 실제는 discount=0, payable=10000이었다.
warning은 Starlette TestClient의 AnyIO BlockingPortal 관련 DeprecationWarning이며 실패 원인은 할인 본문 불일치이다.
수정 후 재실행은 수행하지 않았다. 이번 요청 범위에 따라 기존 구현을 유지했다.
