from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json

app = FastAPI()

# HTML 파일 serve를 위해 static 파일 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 방명록 데이터 모델
class GuestbookEntry(BaseModel):
    name: str
    message: str

# 방명록 데이터 저장 리스트
guestbook_entries = []

# 방명록 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return await request.app.state.jinja_env.get_template("guestbook.html").render_async()

# 방명록 데이터 저장
@app.post("/guestbook")
async def save_guestbook_entry(entry: GuestbookEntry):
    guestbook_entries.append(entry.dict())
    return {"message": "Entry saved successfully"}

# 방명록 데이터 불러오기
@app.get("/guestbook")
async def get_guestbook_entries():
    return guestbook_entries
