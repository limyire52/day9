"""실행: python lesson1-4_selfcheck.py

TestClient로 API를 검사하므로 서버를 따로 실행하지 않아도 됩니다.
각 검사는 PASS를 출력하며 실패하면 AssertionError로 원인을 알려줍니다.
"""

from pathlib import Path
import runpy

from fastapi.testclient import TestClient


def check(response, status_code, expected=None):
    assert response.status_code == status_code, (
        f"예상 상태: {status_code}, 실제: {response.status_code}, "
        f"응답: {response.text}"
    )
    if expected is not None:
        assert response.json() == expected, response.json()


def main():
    # 파일명에 하이픈이 있어서 일반 import 대신 파일 경로로 불러옵니다.
    api_path = Path(__file__).resolve().with_name("lesson1-4_self.py")
    namespace = runpy.run_path(str(api_path))

    with TestClient(namespace["app"]) as client:
        response = client.get("/tasks")
        check(response, 200)
        initial = response.json()
        assert len(initial) == 2, initial
        for task in initial:
            assert task["id"] >= 1 and task["name"] and task["message"]
        check(client.get("/tasks/1"), 200, initial[0])
        print("PASS: 전체 조회 / 개별 조회")

        response = client.post(
            "/tasks", json={"name": "등록", "message": "새 작업"}
        )
        check(response, 201)
        created = response.json()
        task_id = created["id"]
        assert task_id > max(task["id"] for task in initial), created
        check(client.get(f"/tasks/{task_id}"), 200, created)
        print("PASS: 생성 / 중복 없는 ID")

        url = f"/tasks/{task_id}"
        replaced = {"id": task_id, "name": "교체", "message": "전체 수정"}
        check(client.put(url, json={"name": "교체", "message": "전체 수정"}), 200, replaced)
        check(client.put(url, json={"name": "필드 누락"}), 422)
        check(client.get(url), 200, replaced)
        print("PASS: PUT 전체 수정 / 필수 필드 검증")

        patched = {"id": task_id, "name": "이름만 수정", "message": "전체 수정"}
        check(client.patch(url, json={"name": "이름만 수정"}), 200, patched)
        check(client.patch(url, json={}), 200, patched)
        patched["message"] = "메시지만 수정"
        check(client.patch(url, json={"message": "메시지만 수정"}), 200, patched)
        print("PASS: PATCH 부분 수정 / 생략한 필드 유지")

        for field in ("name", "message"):
            for invalid_value in ("", None):
                body = {"name": "검증", "message": "검증", field: invalid_value}
                check(client.post("/tasks", json=body), 422)
                check(client.put(url, json=body), 422)
                check(client.patch(url, json={field: invalid_value}), 422)
        check(client.post("/tasks", json={"name": "메시지 누락"}), 422)
        check(client.get(url), 200, patched)
        for invalid_id in (0, -1, "abc"):
            bad_url = f"/tasks/{invalid_id}"
            check(client.get(bad_url), 422)
            check(client.put(bad_url, json={"name": "검증", "message": "검증"}), 422)
            check(client.patch(bad_url, json={"name": "검증"}), 422)
            check(client.delete(bad_url), 422)
        print("PASS: 문자열 / ID 입력 검증 / 실패한 요청은 데이터 유지")

        missing_url = f"/tasks/{task_id + 1000}"
        error = {"detail": "Task not found"}
        check(client.get(missing_url), 404, error)
        check(client.put(missing_url, json={"name": "없음", "message": "없음"}), 404, error)
        check(client.patch(missing_url, json={"name": "없음"}), 404, error)
        check(client.delete(missing_url), 404, error)
        print("PASS: 없는 작업은 404 / Task not found")

        # id=1을 삭제해도 id=3인 작업은 남아 있어야 합니다.
        response = client.delete("/tasks/1")
        check(response, 204)
        assert response.content == b"", "204 응답에는 본문이 없어야 합니다."
        check(client.get("/tasks/1"), 404, error)
        check(client.get("/tasks/3"), 200, initial[1])
        check(client.delete("/tasks/1"), 404, error)

        for task in client.get("/tasks").json():
            response = client.delete(f"/tasks/{task['id']}")
            check(response, 204)
            assert response.content == b""
        check(client.get("/tasks"), 200, [])
        response = client.post("/tasks", json={"name": "다시 등록", "message": "빈 목록"})
        check(response, 201)
        assert response.json()["id"] > task_id, response.json()
        print("PASS: ID 기준 삭제 / 204 빈 응답 / 전체 삭제 후 재등록")

    print("ALL PASS: CRUD 복습 검사를 모두 통과했습니다.")


if __name__ == "__main__":
    main()
