# getdesign.md 디자인 받기와 GitHub 수동 반영

확인일: 2026-10-23.
아직 적용할 디자인 이름이나 상세 주소가 선택되지 않아 이 단계에서는 앱의 디자인 파일을 수정하지 않았다.

## 1. 디자인 받기

1. https://getdesign.md/ 에 접속한다.
2. Search all designs에서 원하는 디자인을 찾고 상세 페이지를 연다.
3. Preview에서 색상과 화면 분위기를 확인한다.
4. Download DESIGN.md로 파일을 받는다.
5. 파일 이름이 DESIGN.md인지 확인하고 이 프로젝트의 main.py 옆에 저장한다.
6. 파일을 받는 대신 디자인 상세 페이지 주소를 이 대화에 전달해도 된다.

사이트에서 제공하는 DESIGN.md는 색상·글꼴·간격·구성요소를 설명한 디자인 문서다.
완성된 FastAPI 템플릿이나 자동으로 적용되는 CSS 파일이 아니므로, 문서를 읽고 현재 HTML/CSS에 반영하는 과정이 필요하다.
공식 페이지에 npx 설치 방법도 있지만 이번에는 수동 다운로드를 사용하므로 Node.js나 새 도구를 설치할 필요가 없다.

공식 확인 자료:

- 서비스: https://getdesign.md/
- 상세 페이지 예시: https://getdesign.md/notion/design-md
- 운영팀의 공개 모음: https://github.com/VoltAgent/awesome-design-md

사이트에서 다운로드가 원활하지 않으면 공개 모음의 design-md 폴더에서 원하는 디자인 폴더와 DESIGN.md를 확인할 수 있다.
파일 내용을 직접 저장할 때는 웹페이지 자체가 아니라 Markdown 원문을 저장해야 한다.

## 2. 디자인 적용 시 파일 역할

| 파일 | 역할 | GitHub 업로드 |
|---|---|---|
| DESIGN.md | 선택한 디자인의 기준 문서 | 선택. 이후 디자인 작업 기준으로 함께 보관하면 편리 |
| templates/index.html | 제목·영역·폼·목록의 HTML 구조 | 변경되면 같은 경로의 파일 교체 |
| static/style.css | 색상·글꼴·간격·버튼·반응형 배치 | 변경되면 같은 경로의 파일 교체 |
| main.py | 서버 처리, 글 목록과 알림 일부의 HTML 생성 | 목록 구조 변경 등으로 필요한 경우에만 함께 교체 |
| database.py, requirements.txt | 저장과 의존성 | 화면 스타일만 바꾸는 작업이면 보통 변경 불필요 |

기존의 입력 검증과 폼 POST /entries, 동적 값 치환을 보존하면서 스타일을 적용한다.
templates/index.html의 $notification, $name, $message, $entries, $total, $pagination, $max_entries는 서버와 연결되어 있으므로 임의로 삭제하지 않는다.
브랜드 로고·문구를 가져오기보다 선택한 문서의 색상·간격·구성 원칙을 방명록에 맞춰 적용한다.

## 3. 수정본을 GitHub에 수동으로 반영

디자인 적용이 끝난 뒤 제공받은 수정 파일을 같은 경로에 업로드한다.
로컬 Git 연결, git push, 새 저장소 생성은 필요 없다.

1. Render에 연결한 GitHub 저장소와 배포 Branch를 연다.
2. 저장소에서 앱의 templates 폴더로 이동한다.
3. Add file > Upload files를 선택하고 수정된 index.html을 업로드한다.
4. 변경 내용을 확인하고 Commit changes를 완료한다. 보호된 Branch이면 저장소의 PR 절차를 따른다.
5. 앱의 static 폴더로 이동해 같은 방식으로 style.css를 교체한다.
6. main.py도 변경되었다는 안내가 있을 때만 앱 루트에서 그 파일을 교체한다.
7. DESIGN.md는 선택적으로 앱 루트에 올린다.
8. Render에서 최종 Commit이 배포되었는지 확인하고 브라우저에서 Ctrl+F5로 새로고침한다.

폴더를 열어 개별 파일을 업로드할 때는 해당 파일만 선택한다. 예를 들어 templates 안에서 templates 폴더 전체를 다시 넣어 templates/templates/index.html이 되지 않게 한다.
ZIP을 제공받았다면 압축을 풀고 파일을 업로드한다. ZIP 자체를 저장소에 올려도 Render가 자동으로 앱 파일로 풀어 적용하지 않는다.
data, .venv, 캐시 폴더는 업로드하지 않는다.

GitHub 공식 업로드 안내:
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

## 현재 상태

이번에 추가한 파일은 이 안내 문서 하나다. 디자인 선택 전이므로 HTML/CSS 적용본이나 적용 완료 ZIP은 아직 만들지 않았다.
디자인 이름·상세 주소 또는 받은 DESIGN.md를 전달하면 해당 기준으로 수정 파일과 업로드 목록을 만들 수 있다.
