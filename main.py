import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# .env faylidan o'zgaruvchilarni yuklaymiz
load_dotenv()

# Gemini AI sozlamalari
# GEMINI_API_KEY ni Render settings -> Environment bo'limiga qo'shishni unutmang
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()


# Foydalanuvchidan keladigan savol modeli
class ChatRequest(BaseModel):
    message: str


# 1. API holatini tekshirish (Backend test)
@app.get("/status")
def read_status():
    return {"status": "CyberSecurity AI Mentor is running"}


# 2. Asosiy sahifa (Frontendni ko'rsatish)
@app.get("/")
async def read_index():
    # static papkasi ichidagi index.html faylini qaytaradi
    return FileResponse('static/index.html')


# 3. AI Mentor bilan suhbat funksiyasi
@app.post("/ask")
async def ask_mentor(request: ChatRequest):
    try:
        # AI uchun tizimli ko'rsatma (Persona)
        instruction = (
            "Sen kiberxavfsizlik bo'yicha professional mentorsan. "
            "Foydalanuvchilarga axloqiy xakerlik, tarmoq xavfsizligi va kiber-mudofaa haqida "
            "o'zbek tilida aniq va tushunarli ma'lumot berasan. "
            "Noqonuniy harakatlar so'ralsa, ularni axloqiy doirada tushuntir."
        )

        full_prompt = f"{instruction}\n\nFoydalanuvchi savoli: {request.message}"

        response = model.generate_content(full_prompt)
        return {"answer": response.text}

    except Exception as e:
        return {"answer": f"Xatolik yuz berdi: {str(e)}"}


# 4. Static fayllarni (CSS, JS, Images) ulash
# Diqqat: 'static' papkasi loyiha ildizida bo'lishi shart
app.mount("/static", StaticFiles(directory="static"), name="static")