from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypinyin import Style, lazy_pinyin
from snownlp import SnowNLP

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
)

profile = {
    "heroTitle": "关于Me",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
    "featuredWork": {
        "kicker": "作品",
        "title": "文字实验室",
        "copy": "拼音和情绪，挖掘中文里的细节",
        "linkLabel": "打开作品",
    },
    "identity": {
        "motto": "不忘初心，方得始终",
        "learning": "零到全栈",
    },
}
class AnalyzeRequest(BaseModel):
    text: str
    


@app.get("/api/profile")
def get_profile():
    return profile

def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text
    score = round(SnowNLP(text).sentiments, 2)   
    return {
        "text": text,
        "score": score,
        "label": score_label(score),
        "pinyin":" ".join(lazy_pinyin(text, style=Style.TONE)),
    }