"""CRUD 복습 API.

실행: python lesson1-4_self.py
API 문서: http://127.0.0.1:8000/docs
데이터는 메모리에만 저장되므로 서버를 다시 실행하면 초기화됩니다.
"""

from fastapi import FastAPI, HTTPException, Path, Response
from pydantic import BaseModel, Field, field_validator


app = FastAPI(title="CRUD 복습 API")

# 리스트의 위치(index)와 작업의 id는 서로 다른 값입니다.
tasks: list[dict] = [
    {"id": 1, "name": "공부", "message": "FastAPI 복습하기"},
    {"id": 3, "name": "실습", "message": "CRUD 직접 작성하기"},
]
# 삭제한 ID를 다시 사용하지 않도록 다음 번호를 별도로 관리합니다.
next_task_id = max((task["id"] for task in tasks), default=0) + 1


class TaskCreate(BaseModel):
    # id는 서버에서 자동으로 부여합니다.
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


class TaskPut(BaseModel):
    # PUT에서는 수정 가능한 두 필드를 모두 보내야 합니다.
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


class TaskPatch(BaseModel):
    # PATCH에서는 필드를 생략할 수 있습니다.
    name: str | None = Field(default=None, min_length=1)
    message: str | None = Field(default=None, min_length=1)

    @field_validator("name", "message")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        # 생략과 명시적인 null은 다릅니다. 보낸 값은 문자열이어야 합니다.
        if value is None:
            raise ValueError("문자열을 입력하세요. null은 허용하지 않습니다.")
        return value


def find_task(task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    global next_task_id
    task = {"id": next_task_id, **payload.model_dump()}
    tasks.append(task)
    next_task_id += 1
    return task


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int = Path(ge=1)):
    return find_task(task_id)


@app.put("/tasks/{task_id}")
def replace_task(payload: TaskPut, task_id: int = Path(ge=1)):
    task = find_task(task_id)
    # id는 유지하고, 수정 가능한 필드를 모두 교체합니다.
    task.update(payload.model_dump())
    return task


@app.patch("/tasks/{task_id}")
def patch_task(payload: TaskPatch, task_id: int = Path(ge=1)):
    task = find_task(task_id)
    # 요청에 없는 필드는 기존 값을 유지합니다.
    task.update(payload.model_dump(exclude_unset=True))
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int = Path(ge=1)):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
