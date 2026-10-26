# 무료 배포 준비

> 2026-10-23 추가 조사: 현재 추천은 **alwaysdata Free**입니다. 아래 초기 2개 후보 비교를 확장한 [최신 서비스 비교](HOSTING_COMPARISON.md)와 [alwaysdata CMD 배포 절차](DEPLOY_ALWAYSDATA_CMD.md)를 먼저 읽으세요. 아래 내용은 Render·PythonAnywhere를 검토할 경우의 참고 자료입니다.

확인일: 2026-10-23. 사용자 선택은 '아직 없음 — 앱과 배포 안내부터 준비'입니다.
따라서 계정 생성·실제 업로드·공개 배포·유료 전환은 수행하지 않았습니다.

## 먼저 확인할 조건

이 앱은 Python ASGI(FastAPI) 서버와 쓰기 가능한 SQLite 파일 경로가 필요합니다.
HTML 정적 호스팅만으로는 서버와 DB를 실행할 수 없습니다.
계속 글을 보존하려면 무료 플랜에서 영속 디스크를 제공하는지와 FastAPI 지원 여부를 함께 확인해야 합니다.
이 초기 비교의 두 서비스에는 각각 파일 소실 또는 ASGI 실험 기능 제약이 있습니다. 추가 조사로 찾은 alwaysdata 추천과 판단 근거는 위 최신 서비스 비교에 기록했습니다.

| 대상 | 공식 문서에서 확인한 내용 | 이 앱에 대한 판단 |
|---|---|---|
| Render Free Web Service | 무료 서버 지원. 15분 비활성 후 중지. 재배포·재시작·중지 때 로컬 파일 변경 소실. 무료 서버에는 영속 디스크 없음 | 소실을 허용하는 시연에는 사용 가능. 글을 계속 보관하는 방명록의 영속 저장 요건은 충족하지 못함 |
| PythonAnywhere 무료 계정 | 1개 웹 앱·1개 워커·1개월 만료, 512 MiB 디스크. SQLite 사용 가능. FastAPI용 ASGI는 실험 기능이며 장기 가격이 미확정 | 계정에서 ASGI 생성과 현재 무료 이용 조건을 확인한 뒤 검토. 무료 계정 일반 사양을 ASGI 요금 보장으로 해석하지 않음 |

공식 근거:

- Render 무료 정책: https://render.com/docs/free
- Render FastAPI 안내: https://render.com/docs/deploy-fastapi
- PythonAnywhere 무료 계정: https://help.pythonanywhere.com/pages/FreeAccountsFeatures/
- PythonAnywhere SQLite: https://help.pythonanywhere.com/pages/KindsOfDatabases
- PythonAnywhere FastAPI/ASGI 실험 기능: https://help.pythonanywhere.com/pages/ASGICommandLine/

서비스의 무료 조건은 바뀔 수 있습니다. 유료 저장장치·외부 DB·서버 자동 확장은 이번 구현에 포함하지 않습니다.

## Render를 시연용으로 선택할 경우

아래는 안내이며 실제 배포 결과가 아닙니다. 글이 사라져도 되는 경우에만 선택합니다.

1. 이 폴더의 코드·templates·static·requirements.txt를 Git 저장소에 올립니다. data, .venv, 캐시 파일은 제외합니다.
2. Render에서 Python Web Service를 만들고 Instance Type을 Free로 선택합니다.
3. 저장소 루트가 ai4_section01이라면 Root Directory를 Day1-Day8로 지정합니다. 이 폴더 자체를 별도 저장소로 만들었다면 Root Directory는 비웁니다.
4. Render 서비스의 Environment에 `PYTHON_VERSION=3.12.14`를 등록합니다. 환경변수에는 `3.12`가 아니라 패치 번호까지 지정해야 합니다. 이 프로젝트의 로컬 검증 버전은 3.12.14입니다. 환경변수는 `.python-version`보다 우선하므로 기존 값이 3.14라면 함께 수정합니다. [공식 버전 지정 방법](https://render.com/docs/python-version)
5. Build Command: `python -m pip install -r requirements.txt`
6. Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
7. 저장량이 작은 시연이므로 SQLite 위치는 기본값을 사용합니다. 이 파일이 영속 보관된다고 안내하지 않습니다.
8. 생성된 주소에서 글 작성 → 목록 표시 → 새로고침을 확인합니다. 재시작 뒤 파일 소실은 서비스의 알려진 제약입니다.

### Python 3.14에서 pydantic-core 빌드가 실패할 때

로그의 인터프리터가 `python3.14`이고 오래된 pydantic-core가 `.tar.gz`로 내려받아진 뒤 Rust/Cargo 빌드에서 실패한다면, 먼저 위 환경변수로 Python 3.12.14를 지정합니다.
그다음 Manual Deploy에서 Clear build cache & deploy를 선택해 다시 빌드하고 로그에서 실제 Python 버전을 확인합니다.
Rust 설치나 pip 업데이트를 먼저 시도할 필요는 없습니다.

이 폴더의 `.python-version`도 3.12.14입니다. 다만 Render 공식 문서는 이 파일을 저장소 루트에서 읽도록 안내하므로, 상위 저장소의 하위 폴더로 배포하는 현재 구성에서는 Environment의 `PYTHON_VERSION`을 우선 사용합니다.

현재 이 앱의 requirements.txt는 FastAPI 0.115.12, Pydantic 2.11.5, Uvicorn 0.34.2입니다.
배포 로그에 FastAPI 0.112.0, Pydantic 2.8.2, Uvicorn 0.30.1이 표시된다면 로컬 파일과 다릅니다.
Git 연결 저장소, 배포 Branch, Root Directory, 최신 Commit 및 실제로 읽는 requirements.txt를 확인합니다.
저장소 루트가 ai4_section01이면 Root Directory는 Day1-Day8입니다. 앱 패키지 버전은 이번 조치로 변경하지 않았습니다.

월 무료 사용 시간, 트래픽, 빌드 사용량을 확인하세요. Render 문서는 결제 수단이 없는 계정에서 무료 한도 초과 시 서비스·빌드가 중단될 수 있고, 결제 수단이 있으면 일부 초과 사용량이 과금될 수 있다고 설명합니다.
무료 범위를 유지하려면 유료 옵션을 선택하지 않고 해당 계정의 과금·사용량 설정을 확인해야 합니다. 코드는 과금 API를 호출하거나 결제 설정을 변경하지 않습니다.

## PythonAnywhere를 검토할 경우

우선 해당 계정에서 FastAPI용 ASGI 사이트를 무료로 생성할 수 있는지, 영속 파일 경로·만료 연장 조건·CPU 및 디스크 한도가 어떻게 적용되는지 확인합니다.
일반 WSGI Web 앱 설정에 FastAPI app을 그대로 넣으면 실행되지 않습니다.

공식 ASGI 안내는 pythonanywhere CLI와 API 토큰을 사용한 사이트 생성을 안내합니다. CLI는 현재 프로젝트에 없는 추가 외부 라이브러리이므로 이번에 설치하지 않았습니다.
Codex.md 규칙에 따라 실제로 그 경로를 선택한다면 새 도구 설치 여부를 먼저 사용자에게 묻고 진행합니다. 장기 ASGI 가격이 미정이므로 이 안내를 무료 운영 보장으로 보지 마세요.

## 앱이 자체적으로 제한하는 범위

- 외부 API·외부 DB·파일 업로드·이미지 저장·이메일 전송 없음.
- 이름 20자, 메시지 500자, 글 1,000개. 요청 본문 8 KiB, 목록당 10개.
- CSS·폰트를 위한 외부 CDN 요청 없음. JavaScript 프레임워크·빌드 단계 없음.
- 워커 1개로 운영하도록 안내. 같은 로컬 SQLite 파일에 소규모 요청을 처리하는 구성.
- 상한 도달 시 자동 유료 전환·용량 증설·기존 글 삭제 없이 새 쓰기를 409로 거부.

앱의 작은 저장량은 호스팅 무료 한도 전체를 보장하지 않습니다. 트래픽·환경 패키지·로그 사용량도 계정 사용량에 포함될 수 있습니다.
