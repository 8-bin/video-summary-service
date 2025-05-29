from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import utils.youtube as youtube_utils
import utils.s3 as s3_utils
import utils.transcribe as transcribe_utils
import utils.bedrock as bedrock_utils

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize", response_class=HTMLResponse)
async def summarize(
    request: Request,
    youtube_link: str = Form(...),
    summary_lines: int = Form(5),
    summary_style: str = Form("simple"),
    language: str = Form("ko")
):
    # 1️⃣ 유튜브 다운로드
    mp4_path = youtube_utils.download_video(youtube_link)

    # 2️⃣ S3 업로드
    s3_uri = s3_utils.upload_to_s3(mp4_path)

    # 3️⃣ Transcribe 실행 + 대기
    transcript_text = transcribe_utils.run_transcribe(s3_uri)

    # 4️⃣ Bedrock 요약
    prompt = (
        f"Human: 다음 내용을 {summary_lines}줄로 {summary_style} 스타일로 요약해줘. "
        f"언어는 {language}로 해줘.\n\n내용:\n{transcript_text}\n\nAssistant:"
    )
    summary = bedrock_utils.call_bedrock(prompt)

    return templates.TemplateResponse("result.html", {"request": request, "summary": summary})
